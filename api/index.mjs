import {execSync} from 'node:child_process';

export default async ({body, query, cookies, headers}, {json}) => {
    console.debug(execSync('lottie_convert.py').toString());
    return json({status: true});
}
