# Meeting Notes- Feb 10th 2026

### discussed possible architectures
- Server client
- Repo
- And MVVM for FE
- layered (android app architecture)
- could we say implicit invocation for publisher/subscribers for notifications?
    - we could say that node.js eventEmitter does this or apache kafka if we use them?
- definitely using server client and repository architectues

### identifying attributes per page
- task: what attributes we want from image, what attributes we want for album (eg. id, name, etc etc)
- singular photo: caption, image, location, date added, user id for who added it, the rest of the details like audio, etc can be added for after P4 demo
- profile: picture, name, email, other functionality can be added after P4 demo

### FE remaining tasks:
- amirdha: functionality for plus button (add album, upload photo and camera three options, add flow for new album)
- helena: full view of selected photo and feed view
- alex: profile

### debugging geolocation from image
- first tried: PickVisualMedia, this didn't work as the system never gives you the real file. It gives you a privacy‑sanitized copy: same image pixels, but location (and sometimes other EXIF) is stripped before your app ever sees the bytes.
- next tried: GetContent, again this didn't work as with GetContent() and "image/*", on many devices (especially Android 13+) the system reuses the same Photo Picker UI for a “better” experience so still getting sanitized copy with lat/lon stripped
- finally tried: OpenDocument (ACTION_OPEN_DOCUMENT) and this worked as it uses a different flow: the document picker (“Open from” / “Files” / “Google Photos” as document provider, etc.). It returns a document URI, e.g.:
content://com.android.providers.media.documents/document/image%3A123 For that URI, the system treats it as “user explicitly chose this document” and gives you access to the actual document content with full EXIF, including GPS. No stripping for that URI type.

### taking a look into google maps API and if it's able to extract location from coordinates
- https://developers.google.com/maps/documentation/places/web-service/nearby-search?_gl=1*tnb08e*_up*MQ..*_ga*MTk1ODkwODg0OC4xNzcwNzc0Nzk0*_ga_SM8HXJ53K2*czE3NzA3NzQ3OTMkbzEkZzAkdDE3NzA3NzQ3OTMkajYwJGwwJGgw*_ga_NRWSTWS78N*czE3NzA3NzQ3OTMkbzEkZzEkdDE3NzA3NzUwNDUkajYwJGwwJGgw
```input:
{
  "maxResultCount": 10,
  "locationRestriction": {
    "circle": {
      "center": {
        "latitude": 43.4721,
        "longitude": -80.5381
      },
      "radius": 5
    }
  }
}

output:
      "displayName": {
        "text": "Chungchun Rice Hotdog Waterloo(Korean Style Hotdog)",
        "languageCode": "ko"
      },
```