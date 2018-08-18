#
# Copyright (c) 2017-2018, Richard Mortier <mort@cantab.net>
# @license LICENSE.md
#

# Iterate over all datums, filtering out `mtime`, `name` and a list of URLs
# constructed from the `baseUrl` field concatenated with
# `version/service/product-type` string extracted from `.supportedAPIs`.
# `supportedAPIs` is an object where the keys are valid `service` entries and
# the value for each key is a list of supported `version` strings *except* where
# the `service` is "fca-service-metrics". For that service, the value is a list
# of objects, each of which has `version` and `product-type` keys.

.data[] as $d
| { mtime: .meta.LastUpdated,
    name: $d.name,
    urls: [
      $d.baseUrl
      + "/" + ($d.supportedAPIs | to_entries | .[]
              | if .key != "fca-service-metrics" then
                  .value[] + "/" + .key
                else
                  (.value[] as $v
                  | $v.version + "/" + .key + "/" + $v."product-type"
                  )
                end
              )]}
