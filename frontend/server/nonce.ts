import { Request } from 'express';

const nonceRegExp = /nonce="[\w\-]*"/g;

function getNonce(req: Request) {
  return req.header('X-PP-CSP-Nonce') ?? '';
}

export function replaceNonce(req: Request, content: string) {
  return content.replace(nonceRegExp, `nonce="${getNonce(req)}"`);
}
