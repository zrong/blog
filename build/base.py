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


