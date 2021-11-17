## Scrape module

### Skyscanner
from scrape.skyscanner import Skyscanner
skyscanner = Skyscanner(origin="DFWA", destination="SEAA", start_date="2020-03-24", return_date="2020-03-28")
res = skyscanner.run()