import {execSync} from 'node:child_process';

export default async ({body, query, cookies, headers}, {json}) => {
    try {
        console.debug(execSync('lottie_convert.py').toString());
    } catch (e) {
        console.error(e);
    }
    return json({status: true});
}
