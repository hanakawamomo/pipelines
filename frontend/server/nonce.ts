import { Request } from 'express';

export const NONCE_PLACEHOLDER = '{{ _kfpNonce }}';

const nonceRegExp = new RegExp(NONCE_PLACEHOLDER, 'g');

function getNonce(req: Request) {
  return req.header('X-PP-CSP-Nonce') ?? '';
}

export function replaceNonce(req: Request, content: string) {
  return content.replace(nonceRegExp, getNonce(req));
}
