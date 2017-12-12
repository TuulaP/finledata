# finledata

Experimental script to obtain pictures from finna. Searches images which search word given via 'searchbase' variable and restricts to freely used ones see [Finna API](https://www.kiwi.fi/pages/viewpage.action?pageId=53839221 "Finna API documentation"). The images found are downloaded and copied to the folders based on subjects found for the image.

Usage: 

* Change  _searchbase_ -variable to desired word which is used in searches
* Check that DATAPATH is somewhere sensible, downloads and copies pictures under that folder.
* run the script:  `python getledata.py`


Todo:

* think about search in finna, using of subjects directly?
* searchbase to a command line parameter


