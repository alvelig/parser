import {isNumber} from 'lodash'

export function isValidHttpUrl(string) {
  let url;

  try {
    url = new URL(string);
  } catch (_) {
    return "This doesn't look like a url";
  }

  if (!(url.protocol === "http:" || url.protocol === "https:")) {
    return "This doesn't look like a http link";
  }

  if (url.hostname !== 'twitter.com') {
    return "This doesn't look like a twitter link";
  }

  if(!isNumber(parseInt(url.pathname.split('/status/')[1]))) {
    console.log(url.pathname.split('/status/')[1])
    return "This doesn't look like a tweet link. A tweet link is something like that: https://twitter.com/bellingcat/status/1346989282167119872";
  }
}