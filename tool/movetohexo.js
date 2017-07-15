#!/usr/bin/env node
/**
 * 转换博客内容到 hexo
 * 2017-05-24 zrong 替换 [kml_flashembed] 和 [download]
 * 2017-07-09 zrong 处理静态图片文件
 */

const fs = require('fs-extra')
const klawSync = require('klaw-sync')
const path = require('path')
const yaml = require('js-yaml')
const os = require('os')
const util = require('util')

const workDir = path.join(path.dirname(__filename))
const output = fs.createWriteStream(path.join(workDir, 'movetohexo_stdout.log'))
const errorOutput = fs.createWriteStream(path.join(workDir, 'movetohexo_stderr.log'))
const logger = new console.Console(output, errorOutput)

// 博客所在的工作文件夹
const sourceDir = '/Users/zrong/works/mysite/blog'
// 目标文件夹
const targetDir = '/Users/zrong/works/mysite/hexoblog/source'

const flashRe2 = /\[kml_flashembed ([\s\S]+?)\/?\]([\s\S]*\[\/kml_flashembed\])?/mgi
const dlRe = /\[download .*\]/gi
const paramRe = /(\w+)="([^ ]+)"/
const uploadsRe = /(http:\/\/(www\.)?zengrong.net)?\/wp-content\/uploads/gi
const imageRe = /([\w_\-]+)-\d{1,4}x\d{1,4}\.(png|jpg|gif)/gi
const postRe = /http:\/\/(www\.)?zengrong\.net\/post\/(\d+\.htm)/gi

const filterMD = item => path.extname(item.path) === '.md'
const filterImage = item => path.extname(item.path) === '.jpg' ||
  path.extname(item.path) === '.png' ||
  path.extname(item.path) === '.gif'

var flashNum = 0
var dlNum = 0

function getFiles (dir, filter) {
  let paths = klawSync(dir, { filter: filter, nodir: true })
  return paths
}

function splitParam (line, multi) {
  var params = {}
  for (var param of line.split(/\s/)) {
    var matchObj = param.match(paramRe)
    if (matchObj) {
      // logger.log('matchObj:%s ', matchObj)
      var key = matchObj[1].trim()
      var value = matchObj[2].trim()
      if (multi && multi.sep && multi.key && multi.key === key) {
        params[key] = value.split(multi.sep).map(item => item.trim())
      } else {
        params[key] = value
      }
    }
  }
  return params
}

/**
 * 检查提供的行是否包含参数模式
 * @param re 参数正则表达式
 * @param line 要处理的行的内容字符串
 * @param multi 是否将字符串解析为列表，key 指定要作为列表处理的键名，sep 指定列表分隔符 {key: 'id', sep: ','}
 */
function checkPlugin (re, line, multi) {
  var hasPlugin = re.test(line)
  if (hasPlugin) {
    return splitParam(line, multi)
  }
  return null
}

/**
 * 更新前置选项
 */
function updateFrontMatter (lines, filename) {
  const noValueRe = /(%\w{2})+/
  var frontMatterList = null
  var frontMatterObj = {}
  var lastFrontMatterLine = 0
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i]
    // 第一个空行
    if (!line) {
      frontMatterList = lines.slice(0, i)
      lastFrontMatterLine = i
      break
    }
  }
  if (!frontMatterList) {
    return null
  }
  // 处理 ForontMatter
  for (var j = 0; j < lastFrontMatterLine; j++) {
    line = lines[j]
    var param = line.split(': ')
    var key = param[0].toLowerCase().trim()
    var value = param[1].trim()
    // nickname 不是英文的情况，删除
    if (key === 'nicename') {
      if (noValueRe.test(value)) {
        continue
      }
    }
    // wp 中的附件
    else if (key === 'attachments') {
      // 附件为空的情况，跳过这个键名
      if (value === '$ATTACHMENTS') {
        continue
      }
      value = value.split(/, ?/)
    } else if (key === 'category') {
      key = 'categories'
      // hexo 不支持并列分类，使用第一个分类
      value = value.split(',')[0]
    } else if (key === 'tags') {
      // tags 是多个
      value = value.split(',').map(item => item.trim())
    } else if (key === 'modified') {
      key = 'updated'
    }
    frontMatterObj[key] = value
  }
    // 生成一个新的lines 数组，去掉头部
  var newLines = lines.slice(lastFrontMatterLine)
    // 将新的头部作为一行加入lines 开头
  newLines.unshift('---', yaml.safeDump(frontMatterObj).trim(), '---')
  return newLines
}

/**
 * 更新插件支持的特殊标记（基于行）
 */
function updatePlugin (lines, filename) {
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i]
    var dlParams = checkPlugin(dlRe, line, {key: 'id', sep: ','})
    if (dlParams) {
      logger.log('Download plugin %s found.', filename)
      line = `{% download %}${os.EOL}${yaml.safeDump(dlParams)}{% enddownload %}`
      lines[i] = line
      logger.log('download line: %s', line)
      dlNum++
    }
  }
  return lines
}

/**
 * 更新正文
 */
function updateContent (lines, filename) {
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i]
    if (uploadsRe.test(line)) {
      line = line.replace(uploadsRe, '/uploads')
    }
    // 将wordpress 中类似于 -100x200.jpg 这样的自动图片后缀去掉，直接使用原始图片
    if (imageRe.test(line)) {
      logger.log('update image origin:%s', line)
      var line = line.replace(imageRe, "$1.$2")
      logger.log('update image new:%s', line)
    }
    // 将 http://zengrong.net/post/xxx.htm 改为 http://blog.zengrong.net/post/xxx.htm
    if (postRe.test(line)) {
      logger.log('update post url origin:%s', line)
      var line = line.replace(postRe, "http://blog.zengrong.net/post/$2l")
      logger.log('update post url new:%s', line)
    }
    lines[i] = line
  }
  return lines
}

/**
 * 更新插件支持的特殊标记，基于文本
 */
function updatePluginFlash (content, filename) {
  var time = 0
  var result = null
  while ((result = flashRe2.exec(content)) !== null) {
    var param = splitParam(result[1])
    if (!param.movie) {
      var msg = util.format('无法找到 movie %s, content:%s', filename, content)
      throw new Error(msg)
    }
    var flashTag = `{% flash %}${os.EOL}${yaml.safeDump(param)}{% endflash %}`
    content = content.replace(flashRe2, flashTag)
    if (time === 0) flashNum++
    time++
  }
  if (time > 0) {
    logger.log('found flash filename :%s, time: %s', filename, time)
  }
  return content
}

function updateMDFile (file) {
  let content = fs.readFileSync(file.path, 'utf8', 'r')
  // console.log('progress:%s', file.path)
  let targetFile = path.join(targetDir, '_posts', path.basename(file.path))
    // 更新 Flash Tag
  content = updatePluginFlash(content, file.path)
  var lines = content.split(/\r?\n/g)
    // 更新其他 Tag
  lines = updatePlugin(lines, file.path)
    // 更新 Front Matter
  lines = updateFrontMatter(lines, file.path)
  lines = updateContent(lines, file.path)
  fs.writeFileSync(targetFile, lines.join(os.EOL))
}

function go (start, end) {
  var paths = getFiles(path.join(sourceDir, 'post'), filterMD)
  console.log('start: %s, end: %s', start, end)
  // 处理所有的文件
  if (start === -1 && end === -1) {
    paths.forEach(updateMDFile)
    return
  }
  paths.sort((a, b) => parseInt(path.basename(a.path, '.md')) > parseInt(path.basename(b.path, '.md')) ? 1 : -1)
  for (var file of paths) {
    var index = parseInt(path.basename(file.path, '.md'))
    if (index < start || index > end) continue
    updateMDFile(file)
  }
  logger.log('flashNum: %s, dlNum: %s', flashNum, dlNum)
}

/**
 * 处理所有的图片文件
 */
function goImages() {
  var paths = getFiles(path.join(targetDir, 'uploads'), filterImage)
  for (var file of paths) {
    if (imageRe.test(file.path)) {
      fs.unlinkSync(file.path)
      console.log('delete file: %s', file.path)
    }
  }
}

var start = parseInt(process.argv[2]) || -1
var end = parseInt(process.argv[3]) || (start > -1 ? start : -1)
go(start, end)
//goImages()
