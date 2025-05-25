These are findings based off of the URLs currently contained within `"PDAP/training-urls"` as of 5/24/2025

# Broad findings

## Web pages are inconsistent in what data they contain

Web pages often do not contain information that others do. Not all URLs contain metadata tags, for example, or query parameters. Some web pages make reference to their location, and others do not. 

This complicates the task of machine learning, which often benefits from standardized data. 

Consequently, multiple models may be required, with some models that are better at handling inconsistent data (such as Tree-based models) emphasized over others. 

In some cases, data may need to be modified to ensure a higher level of consistency. For example, because all pages contain at least some words that provide information about the source's content, Bag-Of-Words models that take into account the frequency of different words has a lot of potential for being useful.  

## Locational information is often repeated in multiple parts of a web page

Web pages often reference their location in multiple parts of a web page, including:
- The URL itself
- The metadata (title, description, keywords, author)
- Various parts of the HTML

While in some cases multiple locations may be referenced, generally the location most often referenced is the location associated with the source. This makes the location one of the comparatively easier problems. Many pretrained NLP models, such as SpaCy, are effective at identifying when a location is being referenced. Once locations are found, it is comparatively simple to cross-reference them with our database of known locations and identify the most probable location.

## Dataset is imbalanced towards relevant URLs

Our dataset is considerably imbalanced towards relevant URLs, with 3788 relevant URLs and 500 non-relevant URLs, a ratio of over 7:1.

This compromises straightforward analysis, but can be mediated through some statistical techniques. However, the best solution is to increase the number of non-relevant URLs.

## Balancing the dataset is a non-trivial task.

Increasing the number of non-relevant URLs is not straightforward, as the sort of non-relevant URLs we receive is heavily dependent on our means of obtaining URLs.

For example, targeted google searches will likely return a different kind of non-relevant URL as compared to pulling URLs at random from Common Crawl. And the non-relevant URLs which we receive by manual submission would likely be different as well.

In any ML model we use, the utility of different features will likely change as the distribution of URLs changes as we receive more URLs through some sources and not through others. Because of this, ML models will need to be regularly retrained. 

## Rules-based models can complement ML models.

In some cases, we can apply simple heuristics and non-ML rules-based models to aid or replace ML labeling. Provided the rules are well-founded, this can be more effective than using ML, and more resistant to biases in data. In other cases, we can combine ML models with rules-based features.

Potential avenues include:
- A Machine Learning feature indicating whether the domain of the URL is already in our database, and how the associated URLs are classified.
- Identifying the most-frequently referenced location as the location of the source.
- Creating a blacklist of domains we are highly confident are not relevant (for example, news websites).

## We do not have sufficient data for some ML models.

Deep learning-based models such as Bert gain their strength from training on a large amount of data. Because the number of our URLs are numbered in the thousands, and we are unlikely to increase the number of our URLs by several powers of ten any time soon, deep learning models are likely not to be appropriate.

Instead, we will need to rely on simpler models, such as Tree-based models or Naive Bayes models. 

Such models also have the benefit of being trained more quickly and requiring less computational intensity, making them easier to iterate on and analyze. 

## Some ML models are structurally unsuited to our task

Some models (again, like Bert), are based in natural language processing, which is highly dependent on data being in sentence and paragraph format. HTMl data is often not in such a format. Consequently, such models would be unsuited to our task.

# URL Components

## The majority of schemes are https, and this is unlikely to be relevant.

In a simple count analysis, HTTPS urls outnumbered HTTP urls by a ratio of roughly 3:1

However, this offers little to no insight into the relevancy of a URL, much less a record type, and should be excluded from analysis. 

## Many URLs have domains already in our database

As we accrue more URLs, we can narrow the number of possibilities for new sources of data by cross-referencing with existing URLs in our database, effectively eliminating the need for AI altogether. 

For example, if we have at least one URL we have already positively identified as being from `oceancity.md.gov`, any additional URLs containing `oceancity.md.gov` in the domain and subdomain must be from the same source.

## URL Suffixes often contain location data 

While many sources contain suffixes (`.com`, `.gov`, `.us`, a few contain a `{state_iso}.us` suffix, which makes it easy to identify the resultant state. 

## Domains are often unsegmented location words

Many domains contain unsegmented location words that indicate at least part of the locational data. A random sample is included below:

- `detroitmi`
- `montgomeryohio`
- `southamptontownnypolice`
- `longbeach`
- `cityofmebanenc`

Where this occurs, it *considerably* reduces the ambiguity of the associated location, provided we are able to properly segment the words.

There are tools that often enable segmenting words, including [instant-segment](https://github.com/djc/instant-segment).

## Paths often contain contextual information for relevancy and record labeling

Many URL paths will contain information that indicates the purpose of the URL. For example, many URL paths contain some variant of the phrase `press-release` (for example, `/police/press-releases/robbery-suspects-arrested-1-/`), which effectively eliminates any ambiguity as to the record type.

The wrinkle is that many paths include various sub-paths or unsegmented words (for example, `/health/news/dchdtorelocatecovid19vaccinationclinics.html`). Words can be segmented with some degree of accuracy, however. 

A bag of words or keyword or key-phrase detection model may be useful here. 

## Query Parameters are rare and often don't contain useful information

Of the URLs able to be scraped, only 145 contains query parameters. Of these, some contain some information, but most contain information internally relevant to the system (for example, `?qid=126`) but not relevant to the end user, or to us in labeling or determining relevancy. Examples include:
- `?qid=126`
- `?r=eyJrIjoiYmJjZmUwMTEtODY2NS00MGEyLWI0YTctYTVlYzkzYWNlODc3IiwidCI6Ijk0NGZhOWJhLTg0NTQtNDEzZC1iOWU2LWJmNDBhZjFkNmE5YiJ9`
- `?parentIncidentTypeIds=149,150,148,8,97,104,165,98,100,179,178,180,101,99,103,163,168,166,12,161,14,16,15`

Very rarely, information is present, typically in the form of either coordinates or keywords, that provide potentially relevant information. Examples include:
- https://data.detroitmi.gov/datasets/rms-crime-incidents/explore?location=42.353017%2C-83.099036%2C11.04&showTable=true
- https://www.dallasopendata.com/browse?category=Public+Safety
- https://communitycrimemap.com/?address=Sacramento,CA&crimeTypes=%5B1,2,4,6,7,8,10,11,12,14,15,16,17,18%5D&startDate=7&endDate=0

These are rare, however. Possibly too rare for them to be useful for machine learning. They should be de-emphasized in analysis and training.

## Fragments are very rare and almost never contain useful information.

[URL Fragments](https://en.wikipedia.org/wiki/URI_fragment) are occasionally included in URLs, but they almost never contain any useful information. Of the URLs able to be scraped, only 17 fragments were found, including:

- `:~:text=Use of Force Policy&text=Officers are trained to utilize,the weapons, tactics or techniques.`
- `30263860-2020`
- `CLERYMenu`
- `182281928-use-of-force-incidents`

Additionally, since our data sources normally break down record types by page, rather than sections of a page (and fragments typically denote only a section of a page), fragments are often too granular to be useful.

While fragments are rare, they should usually be excluded from analysis. If URLs contain fragments, it is best to remove them prior to ingesting them into ML models.

## Many URLs contain file formats that indicate how to scrape them. 

Of the URLs analyzed, 452 contained file format suffixes. Most of these were `.html`, `.aspx`, `.php`, `.htm`, and other common file extensions indicating HTML data. 


In some cases, however, they indicated other file formats that would indicate a different approach should be taken. These include:

- `.csv` (22 URLs)
- `.xml` (4 URLs)
- `.json` (43 URLs)

These file formats would likely need to be approached using ML models. However, as can be seen above, these were few and far between.

Very rarely, image formats such as `.png` or `.jpg` are included. Such results are almost assuredly irrelevant (and may be among the fastest URLs to break) and should be immediately considered irrelevant or invalid.

# HTML Metadata

## Titles are usually present and often rich in information. 

Titles were present in 2215 URLs, and sometimes contained information relevant for labeling, such as:

- https://www.newcastlewa.gov/departments/police/solicitors: `Solicitor Permits - City of Newcastle`
- https://www.edmondswa.gov/government/departments/police_department/public_information/can_you_i_d_me_: `Can You ID Me - Home`
- https://www.osc.state.ny.us/state-agencies/payroll-bulletins/state-police/sp-130-2010-state-police-expertise-pay: `State Police Bulletin No. SP-130 | Office of the New York State Comptroller`

In some cases, the titles are generic for the website, which can aid in identifying the associated agency/location, but cannot indicate relevancy otherwise. These can be identified as they usually contain locational information. For example:

- http://www.longbeach.gov/police/press-releases/murder-7-/: `City of Long Beach`
- https://police.greenvillesc.gov/1996/getting-here-parking: `Police Department | Greenville, SC - Official Website`
- https://wyoming.delaware.gov/police-department/irma/: `Irma - Town of Wyoming`

## Descriptions are more rare, and sometimes useful where present.

Metadata descriptions were present in 607 URLs. Of these, some clearly indicated information about the URL.

Examples include:
- https://www.floresvilletx.gov/departments/police/complaints-commendations/: `Our complaint system and disciplinary procedures subject Floresville police officers to corrective action and protect them from unwarranted criticism.`
- https://southamptontownnypolice.gov/206/printable-permit-applications: `View an explanation of different permits and how you can apply for them.`
- https://www.coppelltx.gov/389/crime-prevention: `Access information on how to protect yourself and your community from crime.`

However, like with `titles`, many are generic or unclear in their relation to the web page:

- https://police.greenvillesc.gov/304/health-wellness:
- https://www.sandiego.gov/police/contact/meeting-request: `In completing your request, please be as comprehensive, detailed and specific as possible in your responses to questions included on the form. An acknowledgement of your request will be provided to you by email. While we appreciate a need for certainty regarding your request, please be assured that additional phone calls or invitations are not necessary unless requested. Please note that we cannot confirm events more than 6-8 weeks in advance. This form is used in a review process and is not a confirmation for the Chiefs attendance.` 
- https://police.greenvillesc.gov/874/transparency-portal: `Learn about the Police Department and how it serves city residents.`
- https://icjia.illinois.gov/about/publications/a-profile-of-the-illinois-state-police-motor-vehicle-theft-intelligence-clearinghouse/: `Illinois Criminal Justice Information Authority` 

## Keywords are rare, and inconsistently used

Keyword metadata was present in only 125 web pages. Examples include:

- https://ridgelandsc.gov/police-department/daily-arrest-reports-may: `Town of Ridgeland` 
- https://www.southamptontownnypolice.gov/608/animal-control: `Animal Control dogs cats`
- https://www.southamptontownnypolice.gov/137/town-council-office: `Town Council Members,Michael A. Iasilli,Councilperson William Pell IV,Councilperson Cyndi McNamara,Councilperson Tommy John Schiavoni,Councilperson,`
- https://www.minneapolismn.gov/government/departments/police/professional-standards/discipline-matrix/: `Minneapolis, police, discipline matrix, discipline, category, categories, police discipline, officer discipline, disciplinary decisions, internal affairs, discipline imposed, officer conduct, conduct, matrix, MPD, minneapolis, Minneapolis police`

As can be seen, keyword format was inconsistent, and was often treated as an extension of metadata title or description. These can be useful for analyses using word count frequency, but otherwise should be approached with caution.

## Author metadata is very rare, and sometimes contains locational information.

Of the web pages analyzed, only 83 made use of the `Author` metadata. Examples include:

- https://santabarbaraca.gov/government/departments/santa-barbara-police-department:  `Police`
- https://ridgelandsc.gov/police-department/daily-crime-reports-march-2022: `Town of Ridgeland`
- https://bpd.crimegraphics.com/2013/default.aspx: `Sun Ridge Systems, Inc`

Where relevant information is included, it usually related to the location of the web page.

## HTML Bag Of Words

### Location Name Frequency is a highly reliable means of determining the location of a web page

Multiple location names are often found on a web page, but the name associated with the location is very often the most frequent entity. 

For example, in https://www.jacksonms.gov/documents/mayoral-executive-order-amending-the-city-of-jackson-police-departments-use-of-force-policy/, the following terms occur with the following frequency:

| Term | Frequency |
| --- | --- |
|Jackson|3|
|Mississipii| 2|
|MS|2|
|City of Jackson| 1|

Some web pages may not provide all information about a location, but still contain some, for example, URLs for http://www.longbeach.gov includes multiple mention of the name "Long Beach", but rarely if ever mention "California", the state it is in.

Consequently, when determining relevant agencies, location name frequency should be used as a primary indicator of a web page's location. An ML model may not be needed at all, aside from the SpaCy model used to classify words as locations.

### Many non-relevant URLs contain the word `police`

Many non-relevant URLs contain the word `police` in their web pages or URLs. Examples include:

- https://www.newcastlewa.gov/departments/police/solicitors
- https://www.southamptontownnypolice.gov/608/animal-control
- https://estespark.colorado.gov/departments/police/operations/patrol/code-enforcement/report-a-potential-code-violation

In many cases, these are either related to routine enforcement of non-criminal laws or police are incidentally mentioned as part of a broader suite of topics.

### URLs that contain the word `police` are substantially more likely to be relevant

Of URLs that contained the word police at least once, (89%) were relevant and (11%) were not relevant.

The same holds true for other terms, including:
- `department`: 84% vs 16%
- `service`: 83.3% vs 16.7%
- `report`: 88.1% vs 11.9%

NOTE: This is compromised by the fact that our dataset is substantially biased towards relevant-URLs. Reapply this analysis after applying stratified analysis (AKA, calculate proportions of frequencies separately for relevant and non-relevant URLs).

### Some words exist substantially more in non-relevant URLs than in relevant URLs

In many cases, relevant records are identifiable by the words they *don't* have rather than the words they do.

When normalizing by URL count, words that exist substantially more in non-relevant URLs include:
- `play` (2% in relevant vs. 13% in non-relevant)
- `recovery` (1.4% vs. 13.4%)
- `reserve` (4.8% vs. 15%)
- `government` (9.3% vs 30.4%)

NOTE: This is compromised by the fact that our dataset is substantially biased towards relevant-URLs. Reapply this analysis after applying stratified analysis (AKA, calculate proportions of frequencies separately for relevant and non-relevant URLs).
