import os
import platform
import shutil
from ftplib import FTP
from zrong.base import DictBase,slog,writeByTempl

class BlogError(Exception):
    pass

class Conf(DictBase):

    def init(self, workDir, templ, confFile):
        self._setOriginal(workDir, templ, confFile)
        self.saveToFile()

    def _setOriginal(self, workDir, templ, confFile):
        isWindows = platform.system().find("Windows")>-1
        distDir = os.path.abspath(os.path.join(workDir, "distribution"))
        buildDir = os.path.abspath(os.path.join(workDir, "build"))
        writeByTempl(templ, confFile, {
            'IS_WINDOWS':str(isWindows), 
            'CONF_FILE':confFile,
            'DIR_WORK':workDir,
            'DIR_DIST':distDir,
            'DIR_BUILD':buildDir,
            'DIR_TEMPL':os.path.abspath(os.path.join(workDir, "template")),
            'CONFIG_PATH':os.path.abspath(os.path.join(workDir, 
                os.pardir, 'config')),
            'RES_PATH':os.path.abspath(os.path.join(workDir, 
                os.pardir, 'resource')),
            'DT_PATH':os.path.abspath(os.path.join(workDir, 
                os.pardir, 'data_tester')),
            'PYTHON2': r'D:\python\2.7\python.exe' \
                if isWindows else '/usr/bin/python',
            'PHP': os.path.join(buildDir, 'bin', 'quick', 'win32', 'php.exe') \
                if isWindows else 'php',
            'TP': r'D:\PortableApps\TexturePacker\TexturePacker.exe' \
                if isWindows else \
                '/Applications/TexturePacker.app/Contents/MacOS/TexturePacker',
            })
        self.readFromFile(confFile)

    def saveToFile(self):
        super(Conf, self).saveToFile(self.conf_file)

    def getDir(self, name, *path):
        adir = self.dir_conf[name]
        if path:
            return os.path.abspath(os.path.join(adir, *path))
        return adir

    def getExe(self, name, checkExistence=False):
        exe = self.exe_conf[name]
        if checkExistence and exe:
            if not shutil.which(exe, mode=os.X_OK|os.F_OK):
                return None
        return exe

    def getPath(self, *paths):
        return self.getDir("work", *paths)

    def getGit(self, name, key=None):
        git = self.git_conf.get(name)
        if git and key:
            return git.get(key)
        return git

    def getFTP(self, ftpConf, startPath=None, debug=0):
        slog.info("Connecting FTP server %s ......", ftpConf.server)
        ftpStr = 'ftp://%s/'
        if startPath:
            ftpStr = (ftpStr+'%s/')%(ftpConf.server, startPath)
        else:
            ftpStr = ftpStr%ftpConf.server
        ftp = FTP(ftpConf.server, ftpConf.user, ftpConf.password)
        ftp.set_debuglevel(debug)
        if startPath:
            ftp.cwd(startPath)
        serverFiles = ftp.nlst()
        slog.info('There are some files in %s:\n[%s]'%(ftpStr, ', '.join(serverFiles)))
        return ftp, ftpStr

def checkFTPConf(ftpConf):
    if not ftpConf \
    or not ftpConf.server \
    or not ftpConf.user \
    or not ftpConf.password:
        raise HHLError('ftpConf MUST contains following values:'
                'server,user,password !')

def checkEnv(conf):
    if not shutil.which("git", mode=os.X_OK):
        if conf.is_windows:
            slog.error("git is unfindable. "
                'If you are using "Git for windows", please add '
                r'"C:\Program Files (x86)\Git\cmd" '
                "to PATH.")
        else:
            slog.error("git is unfindable.")
        return False

    for exe in conf.exe_conf.keys():
        if not conf.getExe(exe, True):
            slog.error('%s is unfindable. '
                'Please set its path in build_conf.py'%exe)
            return False

    return True

def checkArgs(argv=None):
    parser = argparse.ArgumentParser()
    subParsers = parser.add_subparsers(dest='sub_name', help='sub-commands')

    parserAdmin = subParsers.add_parser('admin', 
        help='For administrator(zrong) only.')
    parserAdmin.add_argument('-a', '--all', action='store_true', 
        help='Perform all of actions.')
    parserAdmin.add_argument('-c', '--cocos', action='store_true', 
        help='Build cocos2d-x zip file and upload it to server 18.')
    parserAdmin.add_argument('-l', '--lua', action='store_true', 
        help='Build lua framework zip file and upload it to server 18.')
    parserAdmin.add_argument('-r', '--res', action='store_true', 
        help='Build resources zip file and upload it to server 18.')
    parserAdmin.add_argument('--tolua', type=str,
        choices = ['auto', 'manual', 'all'],
        help='Build lua binding files. The value is [auto|manual|all].')
    parserAdmin.add_argument('--doc', type=str, 
        choices = ['client', 'zrong', 'all'],
        help='Build documents and upload them to server 18. '
        'The value is [client|build|all].')

    parserInit = subParsers.add_parser('init', help='Initializa HHL project.')
    parserInit.add_argument('--refresh', action='store_true', 
        help='1. Regenerate the build_conf.py file. '
        '2. Install the newest python modules. '
        'It will dismiss all other actions.')
    parserInit.add_argument('-f', '--force', action='store_true', 
        help='Discard all modification and force initialization.')
    parserInit.add_argument('-a', '--all', action='store_true', 
        help='Initialize all repostories and libraries.')
    parserInit.add_argument('-r', '--resource', action='store_true', 
        help='Initialize resource repository.')
    parserInit.add_argument('-c', '--config', action='store_true', 
        help='Initialize config repository.')
    parserInit.add_argument('-d', '--data_tester', action='store_true', 
        help='Initialize data_tester repository.')

    parserUpdate = subParsers.add_parser('update', 
        help='Update all git repostory and library.')
    parserUpdate.add_argument('-f', '--force', action='store_true', 
        help='perform "git reset --hard" in a repostory an pull it.')
    parserUpdate.add_argument('-a', '--all', action='store_true', 
        help='Update all.')
    parserUpdate.add_argument('--cocos', action='store_true', 
        help='Update cocos2d-x framework.')
    parserUpdate.add_argument('--lua', action='store_true', 
        help='Update lua framework.')
    parserUpdate.add_argument('--res', action='store_true', 
        help='Update all resource through server 18. '
        'The command will download a zip file form server 18, '
        'then extract it to "client/res".'
        'These resources are uploaded by zrong, '
        'you can use them for test reason.')
    parserUpdate.add_argument('-s', '--submodule', action='store_true', 
        help='Update all  submodules.')
    parserUpdate.add_argument('-r', '--resource', action='store_true', 
        help='Update git repository of "resource".')
    parserUpdate.add_argument('-c', '--config', action='store_true', 
        help='Update git repository of "config".')
    parserUpdate.add_argument('-d', '--data_tester', action='store_true', 
        help='Update git repository of "data_tester".')

    parserTempl = subParsers.add_parser('templ', 
        help='Generate file by template.')
    parserTempl.add_argument('-n', '--templ-sub-name', required=True,
        help='Give a sub-name for template.')
    parserTempl.add_argument('-a', '--all', action='store_true', 
        help='Generate all files.')
    parserTempl.add_argument('-r', '--resinfo', action='store_true', 
        help='Generate resinfo.lua.')

    parserRes = subParsers.add_parser('res', 
        help='Process resources.')
    parserRes.add_argument('-f', '--force', action='store_true', 
        help='Remove directory before process.')
    parserRes.add_argument('-a', '--all', action='store_true', 
        help='Process all resources.')
    parserRes.add_argument('-l', '--plst', type=str, nargs='*',
        help='Process picture plist files.')
    parserRes.add_argument('-d', '--pdir', type=str, nargs='*',
        help='Process picture dir files.')
    parserRes.add_argument('-r', '--arm', type=str, nargs='*',
        help='Process armature files.')
    parserRes.add_argument('-n', '--fnt', type=str, nargs='*',
        help='Process font files.')
    parserRes.add_argument('-p', '--par', type=str, nargs='*',
        help='Process particle files.')
    parserRes.add_argument('-s', '--snd', type=str, nargs='*',
        help='Process sound files.')
    parserRes.add_argument('-i', '--ani', type=str, nargs='*',
        help='Process animation files.')
    parserRes.add_argument('--lang', type=str, 
            default='zh_cn', choices=['zh_cn'],
        help='Process specified language.')
    parserRes.add_argument('--density', type=str, 
            default='sd', choices=['sd'],
        help='Process specified density.')
    parserRes.add_argument('--vendor', type=str, 
            default='team1201', choices=['team1201'],
        help='Process specified vendor.')

    parserAndroid = subParsers.add_parser('android', 
            help='Android packaging tools.')
    parserIOS = subParsers.add_parser('ios', help='iOS packaging tools.')

    args = parser.parse_args(args=argv)
    if args.sub_name:
        return args, subParsers.choices[args.sub_name]
    parser.print_help()
    return None, None
