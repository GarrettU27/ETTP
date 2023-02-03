import {read as readMat} from 'mat-for-js';
const fs = require('graceful-fs');
const path = require('path');

const MATLAB_FILE_EXTENSION = ".mat";
const HEADER_FILE_EXTENSION = ".hea";

async function ls(inputPath) {
    const dir = await fs.promises.opendir(inputPath)
    for await (const dirent of dir) {
        const direntPath = path.resolve(dir.path, dirent.name);

        if(dirent.isDirectory()) {
            ls(direntPath);
        } else if (dirent.isFile()) {
            const fileExtension = path.extname(dirent.name);
            // console.log(fileExtension)

            if (fileExtension == MATLAB_FILE_EXTENSION) {
                fs.readFile(direntPath, null, (err, data) => {
                    if (err) {
                        console.error(err)
                    }
                    else {
                        const buffer = new Uint8Array(data);
                        const array = readMat(buffer);
                        console.log(array);
                    }
                })
            } else if (fileExtension == HEADER_FILE_EXTENSION) {

            }
        }

    //   console.log(direntPath)
    }
  }

  ls('../server');