const bucketPrefix = "https://earthstripes.s3.us-east-2.amazonaws.com/v3/"

// data acquired from query params that doesn't require json file
const canonicalUrl = document.querySelector("link[rel='canonical']").getAttribute("href");

const urlParams = new URLSearchParams(window.location.search);
var state = URL_PARAMS.get('state');
var county = URL_PARAMS.get('county');
var country = URL_PARAMS.get('country');

const countriesWithStates = ['AU','BR','CA','CN','IN','RU','US']
if (countriesWithStates.includes(country)){
if (!(county == null || county == "false")) {
    county = county.replaceAll(" ", "+")
    var imageID = country+"/"+state+"/"+county+"+"+state
}
else if (!(state == null || state == "false")){
var imageID = country+'/'+state
}
else {var imageID = country}
}
else {var imageID = country}
console.log(county)
console.log(imageID)
document.getElementById('image1').src = bucketPrefix + "stripes/" + imageID+'.png';

const script = document.createElement('script');
script.setAttribute('type', 'application/ld+json');
script.textContent = `
    {
      "@context": "https://schema.org/",
      "@type": "ImageObject",
      "contentUrl": "`+bucketPrefix + "stripes/" + imageID+'.png'+`",
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "acquireLicensePage": "https://www.earthstripes.org/content-license"
    }
`;
document.head.appendChild(script);

label.innerText = country + "  › ";
label.href = "?country=" + country;
label2.innerText = state;
label2.href = "?country=" + country + "&state=" + state;

function generateURL(countryCode = null, stateCode = null, countyName = null) {
    locationAutomaticURL = "/result/?country=" + countryCode;
    if (stateCode != false && stateCode != null) {
        locationAutomaticURL = locationAutomaticURL + "&state=" + stateCode;
    }
    if (countryCode == "US" && countyName != null && countyName != false) {
        locationAutomaticURL = locationAutomaticURL + "&county=" + countyName;
    }
    return locationAutomaticURL;
}

function getCountryFromCountryCode(countryCode){
    const regionNamesInEnglish = new Intl.DisplayNames(['en'], {type:'region'});
    return regionNamesInEnglish.of(countryCode);
}

function breadcrumbs(){
    breadcrumbHTML = ""
    breadcrumbSeparator = '<i class="separatorIcon fa fa-chevron-right"></i>'
    breadcrumbs = [];
    breadcrumbsURLs = [];
    breadcrumbsSchema = ""
    countryName = getCountryFromCountryCode(country);
    if (country && state){
        breadcrumbs.push(country)
        breadcrumbHTML += "<a href=https://www.earthstripes.org"+generateURL(country)+">" + countryName + "</a>"+ breadcrumbSeparator;
    }
    if(country){
      breadcrumbsSchema += `    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "`+countryName+`",
        "item": "https://www.earthstripes.org`+generateURL(country)+`"
      }`
    }
    if (state && county){
      breadcrumbs.push(state)
      breadcrumbHTML += "<a href=https://www.earthstripes.org"+generateURL(country,state)+">" + state + "</a>" + breadcrumbSeparator;
    }
    if (state){
      breadcrumbsSchema += `,{
      "@type": "ListItem",
      "position": 2,
      "name": "`+breadcrumbs[1]+`",
      "item": "https://www.earthstripes.org`+generateURL(country,state)+`"
      }`;
    }
    if (false){
        //breadcrumbs.push(county)
        breadcrumbHTML += "<a href=https://www.earthstripes.org"+generateURL(country,state,county)+">" + county.replaceAll("+"," ") + "</a>" + breadcrumbSeparator;
    }
    if (county){
      breadcrumbs.push(county.replaceAll("+"," "))
      breadcrumbsSchema += `,{
      "@type": "ListItem",
      "position": 3,
      "name": "`+breadcrumbs[2]+`",
      "item": "https://www.earthstripes.org`+generateURL(country,state,county)+`"
      }`
    }
    breadcrumbSpan.innerHTML = breadcrumbHTML;
    console.log(breadcrumbs)
    
    
    const breadcrumbsScript = document.createElement('script');
    breadcrumbsScript.setAttribute('type', 'application/ld+json');
    breadcrumbsScript.textContent = breadcrumbsSchema + "]}";
    test44 = `
    {"@context": "https://schema.org",
    "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "`+breadcrumbs[0]+`",
        "item": "https://www.earthstripes.org`+generateURL(country)+`"
      },{
        "@type": "ListItem",
        "position": 2,
        "name": "`+breadcrumbs[1]+`",
        "item": "https://www.earthstripes.org`+generateURL(country,state)+`"
      },{
        "@type": "ListItem",
        "position": 3,
        "name": "`+breadcrumbs[2]+`",
        "item": "https://www.earthstripes.org`+generateURL(country,state,county)+`"
      }]
    }
    `
    document.head.appendChild(breadcrumbsScript);
}
breadcrumbs();

// this operates the buttons that switch from Stripes to Bars
function switchStripes(switchTo) {
  if (switchTo == 'stripes'){
    document.getElementById('image1').src = bucketPrefix + "stripes/" + imageID + '.png';
  }
  if (switchTo == 'bars'){
    document.getElementById('image1').src = bucketPrefix + "labeled-bars/"+imageID+'.png';
  }
}

// fetches the smallest location json file
var data = "";
fetch(bucketPrefix + "json/" + imageID + ".json")
.then(function (u) {return u.json();})
.then(function (json) {
  data_function(json); // calling and passing json to another function data_function
});

// deals with local impacts
function setLocalImpacts(data){
    if (country == "US" && typeof state == "string") {
        function combineParagraphs(index) {
            text = "";
            for (i = 0; i < data[index]["content"].length; i++) {
            text = text + data[index]["content"][i] + "\n\n";
            //console.log(text)
            }
            return text;
        }
        
        // set the names of all of the stuff
        for (k = 0; k < data.length; k++) {
            element = document.getElementById("ImpactText" + (k + 1));
            element.innerText = combineParagraphs(k);
            element = document.getElementById("ImpactHeader" + (k + 1));
            element.innerText = data[k]["headline"];
            element = document.getElementById("ImpactPhoto" + (k + 1));
        }
        
        // loop through each impact, if there isn't a photo, hide it, if there is, retrieve it and insert alt text
        for (k = 0; k < data.length; k++) {
        element = document.getElementById("ImpactPhoto" + (k + 1));
                console.log(data[k]["img"]["file"])
            if (data[k]["img"]["file"] == null || data[k]["img"]["file"] == ""){
                element.style.display = "none";
                
                column = document.getElementById("LocalImpactBox" + (k + 1) + "Column1")
                column.style.width = "100%";
                column = document.getElementById("LocalImpactBox" + (k + 1) + "Column2")
                column.style.width = "100%";
            }
            else {
                element.src = bucketPrefix + 'photos/local-impact-photos/'+state+'/' + data[k]["img"]["file"] + ".jpg";
                element.alt = data[k]["img"]["alt"];
            }
        
        console.log(element.height/element.width);
        if (true){//element.height/element.width < 0.5) {
            column = document.getElementById("LocalImpactBox" + (k + 1) + "Column1")
            column.style.width = "100%";
            column = document.getElementById("LocalImpactBox" + (k + 1) + "Column2")
            column.style.width = "100%";
        }
        
        // if there isn't a caption hide it, if there is fill in the data and credit
        element = document.getElementById("ImpactPhotoCaption" + (k + 1));
        if (data[k]["img"]["caption"] == null ){
                element.style.display = "none";
            }
            else {
                element.innerText = data[k]["img"]["caption"] + " Credit: " + data[k]["img"]["credit"] ;
            }
        
        }
        
        // hide empty local impact data boxes
        console.log(8 - data.length);
        for (k = 0; k < 8 - data.length; k++) {
            var box = document.getElementById("LocalImpactBox" + (8 - k));
            console.log("LocalImpactBox" + (8 - k));
            box.style.display = "none";
        }
    } else {
        ImpactBox.style.display = "none";
    }
}

// sets the bars for yale data_function
function setYaleBars() {
    YaleSubHeader.innerText = "How people in " + data["YaleClimateOpinionData2020"]["data"]["GeoName"] + " view climate change";
    datas = ["happening", "personal","harmUS", "congress","fundrenewables","teachGW"];

    for (let i = 0; i < datas.length; i++) {
        var agree1 = document.getElementById("Yaleagree" + (i + 1));
        left = data["YaleClimateOpinionData2020"]["data"][datas[i]];
        agree1.setAttributeNS(null, "width", left);
        agree1text = document.getElementById("Yaleagree" + (i + 1) + "text");
        agree1text.innerHTML = Math.round(left) + "%";
        agree1text.setAttributeNS(null, "x", left - 1);

        var disagree1 = document.getElementById("Yaledisagree" + (i + 1));
        right = data["YaleClimateOpinionData2020"]["data"][datas[i] + "Oppose"];
        disagree1.setAttributeNS(null, "x", 100 - right);
        disagree1.setAttributeNS(null, "width", right);
    }
}

const productNames = ["Cloth Mask","Mug","Tie","Stickers"]
const productIDs = ['256670743725195335','168540946485519042','151119561160107608','217917661479101292']
function setMerchBox(){
  var encodedLabeledStripesImageURL = encodeURI(bucketPrefix + "labeled-stripes/" + imageID + ".png?request=zazzle");
  var encodedStripesImageURL = encodeURI(bucketPrefix + "stripes/" + imageID + ".png?request=zazzle");

  merchLabel = "&t_location_txt=" + encodeURIComponent(locationName + " " + startYear + "-" + endYear);
  customMerchLink = "https://www.zazzle.com/api/create/at-238391408801122257?rf=238391408801122257&ax=DesignBlast&sr=250403062909979961&cg=196064354850369877&t__useQpc=false&t__smart=false&t_labeledstripes_iid="
  + encodedLabeledStripesImageURL + "&tc=results-merch-box&ic=" + imageID.replace(/[^a-zA-z]/g,'_') + "&t_stripes_iid=" + encodedStripesImageURL + merchLabel;
  testmerchlink.href = customMerchLink;
  MerchButton.href = customMerchLink;
  console.log(imageID.replace(/[^a-zA-z]/g,'_'))

  for (i=1; i<=productNames.length; i++){
    element = document.getElementById('ProductImage' + i);
    var imageID2 = 'https://rlv.zazzle.com/svc/view?pid='+productIDs[i-1]+'&max_dim=600&at=238391408801122257&t_stripes_url='+encodedStripesImageURL + '&t_labeledstripes_url='+encodedLabeledStripesImageURL;
    element.src = imageID2;
    element.alt = "Warming Stripes " + productNames[i-1]
    element = document.getElementById('ProductName' + i);
    element.innerText = productNames[i-1];
    element = document.getElementById('Product'+i+"Link");
    element.href = customMerchLink;
    element = document.getElementById('Product'+i+'Link2');
    element.href = customMerchLink;
  }
}

function getSenatorInfo(senatorData) { 
  // fetch civic info function
  fetch(
    "https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyB6RdsMva-gOY7FNxgrrHsBgskpF_a8njc&levels=country&roles=legislatorUpperBody&address=" +
      state +
      ",USA"
  )
    .then(function (u) {
      return u.json();
    })
    .then(function (json) {
      //data_function(json); // calling and passing json to another function data_function
      console.log(json);
      
      senator1json = senatorData[json.officials[0].name]
      SenatorName1.innerText = json.officials[0].name;
      SenatorSubHeading1.innerText = "Senator, " + senator1json["stateName"] + ", " + senator1json["current term readable"] + " term";
      SenatorScore1.innerText = "Overall Score: " + senator1json["overallScore"]+"/100";
      s1positionScore.textContent = senator1json["positionScore"];
      s1voteScore.textContent = senator1json["voteScore"];
      s1leadershipScore.textContent = senator1json["leadershipScore"];
      s1carbonFreeScore.textContent = senator1json["carbonFreeScore"];
      SenatorSite1txt.innerText = json.officials[0]["urls"][0].replace('https://www.','').replace('/','');
      SenatorSite1.href = json.officials[0]["urls"][0];

      senator2json = senatorData[json.officials[1].name]
      SenatorName2.innerText = json.officials[1].name;
      SenatorSubHeading2.innerText = "Senator, " + senator2json["stateName"] + ", " + senator2json["current term readable"] + " term";
      SenatorScore2.innerText = "Overall Score: " + senator2json["overallScore"]+"/100";
      s2positionScore.textContent = senator2json["positionScore"];
      s2voteScore.textContent = senator2json["voteScore"];
      s2leadershipScore.textContent = senator2json["leadershipScore"];
      s2carbonFreeScore.textContent = senator2json["carbonFreeScore"];
      SenatorSite2txt.innerText = json.officials[1]["urls"][0].replace('https://www.','').replace('/','');
      SenatorSite2.href = json.officials[1]["urls"][0];
      
      console.log(JSON.stringify(json));
      // runs the images after in case there are any issues
      //SenatorImage2.src = json.officials[1].photoUrl  //photo from database
      SenatorImage2.src = bucketPrefix + "photos/compressed/senators/" + senatorData[json.officials[1].name]["image"];
      SenatorImage2.alt =  senator2json["stateName"] + " Senator " + json.officials[1].name
      
      //SenatorImage1.src = json.officials[0].photoUrl //photo from database
      SenatorImage1.src = bucketPrefix + "photos/compressed/senators/" + senatorData[json.officials[0].name]["image"];
      SenatorImage1.alt =  senator1json["stateName"] + " Senator " + json.officials[0].name

      console.log(bucketPrefix + "senators/" + senatorData[json.officials[0].name]["image"]
      );
    });
}

function setEnergyGraph(energyData){
  var ctx = document.getElementById("myChart").getContext("2d");

  //console.log(energyData['years']);

  const colors = {
    green: {
      fill: '#5eb84d',
      stroke: '#5eb84d',
    },
    lightBlue: {
      stroke: '#bbbbbb',
      fill: '#bbbbbb',
    },
    yellow: {
      fill: '#FFD000',
      stroke: '#FFD000',
    },
    purple: {
      fill: 'purple',
      stroke: 'purple',
    },
    charcoal: {
      fill: '#323232',
      stroke: '#323232',
    },
  };

  const coal = energyData['coal'];
  const naturalGas = energyData['natural gas'];
  const petroleum = energyData['petroleum and other liquids'];
  const nuclear = energyData['nuclear'];
  const renewables = energyData['renewables and others'];
  const xData = energyData['years'];

  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: xData,
      datasets: [{
        label: "Coal",
        fill: true,
        backgroundColor: colors.charcoal.fill,
        pointBackgroundColor: colors.charcoal.stroke,
        borderColor: colors.charcoal.stroke,
        pointHighlightStroke: colors.charcoal.stroke,
        borderCapStyle: 'butt',
        data: coal,

      }, {
        label: "Natural Gas",
        fill: true,
        backgroundColor: colors.purple.fill,
        pointBackgroundColor: colors.purple.stroke,
        borderColor: colors.purple.stroke,
        pointHighlightStroke: colors.purple.stroke,
        borderCapStyle: 'butt',
        data: naturalGas,
      }, {
        label: "Petroleum",
        fill: true,
        backgroundColor: colors.lightBlue.fill,
        pointBackgroundColor: colors.lightBlue.stroke,
        borderColor: colors.lightBlue.stroke,
        pointHighlightStroke: colors.lightBlue.stroke,
        borderCapStyle: 'butt',
        data: petroleum,
      }, {
        label: "Nuclear",
        fill: true,
        backgroundColor: colors.yellow.fill,
        pointBackgroundColor: colors.yellow.stroke,
        borderColor: colors.yellow.stroke,
        pointHighlightStroke: colors.yellow.stroke,
        data: nuclear,
      }, {
        label: "Renewables & Other",
        fill: true,
        backgroundColor: colors.green.fill,
        pointBackgroundColor: colors.green.stroke,
        borderColor: colors.green.stroke,
        pointHighlightStroke: colors.green.stroke,
        data: renewables,
      }]
    },
    options: {
    responsive: true,
    // Can't just just `stacked: true` like the docs say
    scales: {
      yAxes: {
        stacked: true,
        max: 100,
        min: 0,
      },
    },
    animation: {
      duration: 750,
    },
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: false,
    },
    elements: {
      point: {
        radius: 0,
      },
      line: {
        tension: 0.3,
      },
    },

    }
  });
}


function handleStateJSON(json){
    setLocalImpacts(json["local impacts"]);
    getSenatorInfo(json["SenatorInfo"]);
}

if (country == "US" && typeof state == "string"){

} else {
    legislativeBox.style.display = "none";
}

//function to set related locations
function setRelatedLocations(relLocationsJSON){
    var dataLen = relLocationsJSON['locations'].length;
    //loops through first 5 locations
    for (let i = 1; i <= 5; i++){
        btn = document.getElementById("b"+i)
        btn.innerText = relLocationsJSON['locations'][i-1]
        link = document.getElementById("l"+i)
        link.href = relLocationsJSON['links'][i-1]
        console.log(relLocationsJSON['links'][i-1])
    }
    //hides the remaining locations if less than 5 provided
    for (let i = 5; i > (dataLen-2); i--){
        btn = document.getElementById("b"+i);
        btn.style.display = "none";
        console.log("b"+i)
        
    }
    //sets the state and country
    for (let i = 0; i <= 2; i++){
        b6.innerText = relLocationsJSON['locations'][dataLen-2]
        l6.href = relLocationsJSON['links'][dataLen-2]
        b7.innerText = relLocationsJSON['locations'][dataLen-1]
        l7.href = relLocationsJSON['links'][dataLen-1]
    }
}

// main function that loads JSON data
function data_function(jsonData) {
console.log(jsonData)
// if there is a county (hence in US) and there are no local impacts data for the county, fetch the state data
if (typeof county == "string" && jsonData["local impacts"] == null){
    fetch(bucketPrefix + "json/" + country + "/" + state + ".json")
    .then(function (u) {return u.json();})
    .then(function (json) {
      handleStateJSON(json); //calling and passing json to another function data_function
    });
} else {
    setLocalImpacts(jsonData["local impacts"]);
    
    if (country == "US"){
    getSenatorInfo(jsonData["SenatorInfo"]);
    }

}
data = jsonData;

//alert(data.sentence);
locationName = data.metadata.name;
document.getElementById('image1').alt = "Warming stripes for " + locationName;

if (jsonData["custom properties"] && jsonData["custom properties"]["common name"]){
    myHeader9.innerText = jsonData["custom properties"]["common name"];
} else {
    myHeader9.innerText = locationName;
}
document.title = locationName + " - Earth Stripes"; //changed the title but now we use php

startYear = data.resources.stripes["startYear"];
endYear = data.resources.stripes["endYear"];
description1 = "These warming stripes show the annual temperature change in " + locationName + " from " + startYear + "-" + endYear + ", red and blue stripes represent warmer and cooler temperatures respectively";
img1description.innerText = description1;
image1.alt = "Warming Stripes for " + locationName + " from " + startYear + "-" + endYear;

// sets yale information
try{
    setYaleBars();
}catch (error) {
    console.warn("No Yale Climate Opinion Data Found");
    YaleOpinion.style.display = "none";
}

setMerchBox();

if (data["energy consumption"] == null){
    console.warn("No Energy Data Found");
    energyBox.style.display = "none";
} else {
    setEnergyGraph(data["energy consumption"]);
    energyData = data["energy consumption"];
}

// if recommended/related locations exists in JSON, set them, else hide box
if (data['metadata']['recommended locations']){
    setRelatedLocations(data['metadata']['recommended locations']);
}else {
    relatedLocationsBox.style.display = "none";
}

// this needs to be here cause it needs to get locationName from JSON
tweetContent = "Warming Stripes from @earthstripes show how " + locationName + " is warming. Take a look at your region: " + encodeURI(canonicalUrl);
facebookShareContent = "Warming Stripes from @earthstripes show how " + locationName + " is warming. Take a look at your region: "

}

// social media stuff
// call functions when buttons clicked
document.getElementById('twitter-share-button1').onclick = function() {
gtag('event', "Share Intent", {
  'event_category': "Social",
  'event_label': canonicalUrl,
  'value': "5"
});
window.open("https://twitter.com/intent/tweet?text="+encodeURIComponent(tweetContent)+"&related=earthstripes,nikhilrado&hashtags=showyourstripes,climate", "pop", "width=600, height=400, scrollbars=no");

}
document.getElementById('facebook-share-button1').onclick = function() {
window.open("https://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(canonicalUrl)+"&hashtag=#showyourstripes", "pop", "width=600, height=400, scrollbars=no");

window.open("https://www.facebook.com/dialog/share?app_id=604427890576897&display=popup&href="+encodeURIComponent(canonicalUrl)+"&redirect_uri=https%3A%2F%2Fwww.earthstripes.org"+"&hashtag="+encodeURIComponent("#showyourstripes")+"&quote=" + encodeURIComponent(facebookShareContent), "pop", "width=600, height=400, scrollbars=no");

}

// load twitter SDK
window.twttr = (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
      t = window.twttr || {};
    if (d.getElementById(id)) return t;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);
  
    t._e = [];
    t.ready = function(f) {
      t._e.push(f);
    };
  
    return t;
  }(document, "script", "twitter-wjs"));
  
// Load the Snapchat SDK asynchronously
  (function (d, s, id) {
    var js,
      sjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://sdk.snapkit.com/js/v1/create.js";
    sjs.parentNode.insertBefore(js, sjs);
  })(document, "script", "snapkit-creative-kit-sdk");

  window.snapKitInit = function () {
    snap.creativekit.initalizeShareButtons(
      document.getElementsByClassName("snapchat-share-button")
    );
  };
  
function zazzleClicked(element) {
    console.log("bbbbbbbbbbbbbbbb");
    if (element.includes("Product")) {
        let listId = element.charAt(element.length-1)-1
        element = productNames[listId] + " " + productIDs[listId];
    }
    console.log(element)
    gtag('event', "Zazzle Link Clicked", {
    'event_category': "commerce",
    'event_label': element,
    'value': "5"
    });

};

// taken from https://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}