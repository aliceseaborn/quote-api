title: Version 0
author: Seaborn
date: 2019-10-08


<br>

##### Overview

This API was developed to supplement a developers financial analysis interests. Financial data used to be provided by the major search engines for free through APIs and libraries which were well respected and maintained. After a while, however, these tools were deprecated and could no longer support the needs of financially savvy developers. This API, which relies on screen scraping, provides a method of obtaining information which is already publically available and which used to be provided for free. There is no indication that the information available on Yahoo is protected under copyright and I provide this API with strictly academic and educational intentions. I do not assume liability for the use and/or abuse of this API or its contents.


##### Examples

<div class="alert alert-info" role="alert">
  <b>Note:</b> This API returns JSON formatted output. Alternative return formats are not currently supported.
</div>

This tutorial assumes that `[site]/` is the root endpoint. All APIs are located at `/api` and version zero can be found at `/api/0/`.

| Request                    | Returns                                       |
|----------------------------|-----------------------------------------------|
| `/api/0/get?ticker=xyz`    | The server's current record for XYZ stock.    |
| `/api/0/update?ticker=xyz` | Updates the record for XYZ stock.             |
| `/api/0/create?ticker=xyz` | Updates and returns the record for XYZ stock. |
