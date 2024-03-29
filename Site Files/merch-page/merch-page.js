// gets product data and inserts into page
fetch("https://ortana-test.s3.us-east-2.amazonaws.com/price-info.json")
.then(function (u) {return u.json();})
.then(function (json) {
  processPriceInfo(json); // calling and passing json to another function processPriceInfo
});

// inserts coupon banner info into banner and makes it visible
function processPriceInfo(merchData){
    if (merchData['coupon_code'] && merchData['coupon_code'] != ""){
        var x = document.getElementById('sale-banner');
        x.innerText = merchData['discount'];
        x.style.visibility = "visible";
        couponCode = merchData['coupon_code'];
        
    }
}
// document.getElementById("autocomplete").focus();

// generates random 8 digit padded number as String
const ES_ID = String(Math.round(Math.random()*10**8)).padStart(8, '0')
const URL_PARAMS = new URLSearchParams(window.location.search);
var twclid = URL_PARAMS.get('twclid');
if (!twclid){
    twclid = getCookie("twclid");
}
console.log("twclid: " + twclid);

var fbc = URL_PARAMS.get('fbc');
if (!fbc){
    fbc = getCookie("_fbc");
}
console.log("fbc: " + fbc);

var fbp = URL_PARAMS.get('fbp');
if (!fbp){
    fbp = getCookie("_fbp");
}
console.log("fbp: " + fbp);

var gid = URL_PARAMS.get('gid');
if (!gid){
    gid = getCookie("_gid");
}
console.log("gid: " + gid);


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

var changeLocationBoxIsHidden = true;
function toggleChangeLocation(action=null){
    var element = document.getElementById("changeLocationBox");
    if(changeLocationBoxIsHidden && action!="hide"){
        element.style.display = "block";
        document.getElementById('autocomplete').focus();
        changeLocationBoxIsHidden = false;
    }
    else{
        element.style.display = "none";
        changeLocationBoxIsHidden = true;
    }
    console.log(changeLocationBoxIsHidden)
}

function generateURL(countryCode = null, stateCode = null, countyName = null, loc = null) {
    if (loc){return "/result/?location=" + loc;}
    locationAutomaticURL = "/result/?country=" + countryCode;
    if (stateCode != false && stateCode != null) {
        locationAutomaticURL = locationAutomaticURL + "&state=" + stateCode;
    }
    if (countryCode == "US" && countyName != null && countyName != false) {
        locationAutomaticURL = locationAutomaticURL + "&county=" + countyName;
    }
    return locationAutomaticURL;
}

const COUNTRIES_WITH_STATES = ['AU','BR','CA','CN','IN','RU','US']
function generateImageID (countryCode=null, stateCode=null, countyName=null, loc=null){
    if(loc){return "location/"+loc;}
    var ImageID = countryCode

    if (COUNTRIES_WITH_STATES.includes(countryCode)) {
      if (stateCode != false && stateCode != null) {
        ImageID = ImageID + "/" + stateCode;
      }
      if (countryCode == "US" && countyName != null && countyName != false) {
        ImageID = ImageID + "/" + countyName.replaceAll(" ", "+").replace("St", "St.") + "+" + stateCode;
      }
    }
    return ImageID;
}

function getCountryFromCountryCode(countryCode){
    const regionNamesInEnglish = new Intl.DisplayNames(['en'], {type:'region'});
    return regionNamesInEnglish.of(countryCode);
}

bucketPrefix = "https://earthstripes.s3.us-east-2.amazonaws.com/v3/";

const ZAZZLE_INT_COUNTRIES = ["us","ca","gb","de","es","fr","pt","se","nl","at","ch","be","br","au","nz","jp"];
const ZAZZLE_INT_DOMAINS = [".com",".ca",".co.uk",".de",".es",".fr",".pt",".se",".nl",".at",".ch",".be",".com.br",".com.au",".co.nz",".co.jp"];
function getZazzleDomain(countryCode){
    countryCode = countryCode.toLowerCase();
    zazzleDomain = ZAZZLE_INT_DOMAINS[ZAZZLE_INT_COUNTRIES.indexOf(countryCode)];
    if (zazzleDomain == undefined){
        zazzleDomain = ".com";
    }
    return zazzleDomain;
}

const PRODUCT_NAMES = ["Cloth Mask","Mug","Tie","Stickers", "Magnet","Badge (Pin)", "T-Shirt", "Socks"];
const PRODUCT_IDS = ['256670743725195335','168735114625411268','151119561160107608','217917661479101292','147753984968275362', '145354997245092652', '235484093576644423','256547457460896288'];
function setMerchBox(imageID, locationName, locationURL){
    globalImageID = imageID
    
    var encodedLabeledStripesImageURL = encodeURI(bucketPrefix + "labeled-stripes/" + imageID + ".png?request=24012022");
    var encodedStripesImageURL = encodeURI(bucketPrefix + "stripes/" + imageID + ".png?request=24012022");
    var encodedLightLabeledBarsImageURL = encodeURI(bucketPrefix + "light-labeled-bars/" + imageID + ".png?request=24012022");
    
    
    imageTrackingCode = "mp";
    if (twclid){
        imageTrackingCode += "_twclid" + twclid;
    }
    if (fbp){
        imageTrackingCode += "_fbp"+fbp;
    }
    if (fbc){
        imageTrackingCode += "_fbp"+fbp;
    }
    if(gid){
        imageTrackingCode += "_gid"+gid;
    }
    imageTrackingCode = ES_ID + "_" + imageTrackingCode;
    if (imageTrackingCode.length > 99){
        imageTrackingCode = imageTrackingCode.substr(0,98)
    }
    imageTrackingCode.replaceAll('.','_');

    merchLabel = "&t_location_txt=" + encodeURIComponent(imageID.replaceAll('+',' '));//  + " " + startYear + "-" + endYear);
    customMerchLink = "https://www.zazzle" + getZazzleDomain(countryLang) + "/api/create/at-238391408801122257?rf=238391408801122257&ax=DesignBlast&sr=250403062909979961&cg=196064354850369877&t__useQpc=false&t__smart=false&t_labeledstripes_iid=" + encodedLabeledStripesImageURL + "&tc=" + imageTrackingCode + "&ic=" + imageID.replace(/[^a-zA-z]/g,'_') + "&t_stripes_iid=" + encodedStripesImageURL + "&t_lightlabeledbars_iid=" + encodedLightLabeledBarsImageURL + merchLabel;
    customMerchLink += "&st=date_created"
    console.log(customMerchLink);
    MerchButton.href = customMerchLink;
    console.log(imageID.replace(/[^a-zA-z]/g,'_'));
    
    for (i=1; i<=PRODUCT_NAMES.length; i++){
        element = document.getElementById('ProductImage' + i);
        var imageID2 = 'https://rlv.zazzle.com/svc/view?pid='+PRODUCT_IDS[i-1]+'&max_dim=600&at=238391408801122257&t_stripes_url='+encodedStripesImageURL + '&t_labeledstripes_url='+ encodedLabeledStripesImageURL + '&t_lightlabeledbars_url=' + encodedLightLabeledBarsImageURL;
        element.src = imageID2;
        element.alt = "Warming Stripes " + PRODUCT_NAMES[i-1];
        element = document.getElementById('ProductName' + i);
        element.innerText = PRODUCT_NAMES[i-1];
        element = document.getElementById('Product'+i+"Link");
        element.href = customMerchLink;
        //element = document.getElementById('Product'+i+'Link2');
        //element.href = customMerchLink;
    }
    
    /*
    // This section was created in order to feature new products that didn't yet get through zazzle's systems

    var thingg = document.getElementById("ProductImage31")
    thingg.src = "https://rlv.zazzle.com/svc/view?pid=256511214137703962&max_dim=600&at=238391408801122257&t_largesquarestripes_url=https://earthstripes.s3.us-east-2.amazonaws.com/v3/large-square-stripes/"+imageID+".png?request=zazzle"
    scarfLink = "https://www.zazzle.com/api/create/at-238391408801122257?rf=238391408801122257&ax=Linkover&pd=256511214137703962&ed=false&tc=&ic=&t_largesquarestripes_iid=https%3A%2F%2Fearthstripes.s3.us-east-2.amazonaws.com%2Fv3%2Flarge-square-stripes%2F"+imageID+".png"
    console.log(scarfLink)
    thingg2 = document.getElementById("Product31Link")
    thingg2.href = scarfLink
    thingg3 = document.getElementById("ProductButton31")
    thingg3.href = scarfLink
    */
    
    element = document.getElementById('locationName');
    element.innerText = imageID.replaceAll("+"," ");
    element = document.getElementById('locationNameLink');
    console.log(locationURL);
    element.href = locationURL;
    

    var yeet = document.getElementById("underline-text");
        myArray = imageID.split("/");
        countryCode = myArray[0]
        locationName = myArray[myArray.length - 1].replaceAll("+"," ")
    if (countryCode == locationName && locationName.length == 2){ // if it is just a country code, replace with name
        locationName = getCountryFromCountryCode(locationName);
    } else if (myArray.length >= 3) {
        pos = locationName.lastIndexOf(" ")
        locationName = locationName.substring(0,pos) + ", " + locationName.substring(pos+1)
        
    }
    yeet.textContent = locationName;
    toggleChangeLocation(action="hide");
    
    window.scrollTo(0,0); // scrolls to top of page to avoid layout shifts
} 

// custom function to get Redirect URL
function getRedirectURLMapbox(jsonPlaceData,redirectNow=false) {
    placeName = jsonPlaceData.place_name
    
    // gets the country code of location
    if (jsonPlaceData.place_type[0]=="country"){
        countryCode = jsonPlaceData.properties.short_code
        countryName = jsonPlaceData.text
    }
    else {
        countryCode = jsonPlaceData.context[jsonPlaceData.context.length-1].short_code
        countryName = jsonPlaceData.context[jsonPlaceData.context.length-1].text
    }
    countryCode = countryCode.toUpperCase()
    
    // get stateCode
    if (jsonPlaceData.place_type[0]=="region"){
        stateCode = jsonPlaceData.properties.short_code
        stateName = jsonPlaceData.text
        stateCode = stateCode.slice(3)
    }
    else{
        try{
            stateCode = jsonPlaceData.context[jsonPlaceData.context.length-2].short_code
            stateName = jsonPlaceData.context[jsonPlaceData.context.length-2].text
            stateCode = stateCode.slice(3)
        }
        catch(err) {
            stateCode = false
            stateName = false
        }
    }
    
    // get county
    if (jsonPlaceData.place_type[0]=="district"){
        countyName = jsonPlaceData.text
    }
    else{
        try{
            countyName = jsonPlaceData.context[jsonPlaceData.context.length-3].text
        }
        catch(err) {
            countyName = false
        }
    }

    lowestLocationName = getLowestLocationName(countryCode,stateCode,countyName);

    generateURL(countryCode,stateCode,countyName);
    setMerchBox(generateImageID(countryCode,stateCode,countyName));
    if (redirectNow){
        // window.location.href = locationAutomaticURL
    }

    x.innerHTML = lowestLocationName
    return locationAutomaticURL; 
}

function getLowestLocationName(countryCode,stateCode,countyName){
    // get lowest location name which will be used as the label for the location btn
    lowestLocationName = countryName
    // tried to insert this stuff next to if statement to run when country is just US
    if (countryCode != "US"){
        lowestLocationName = countryName // sets it to country name if not US
    }
    else{
        if (stateCode != false){lowestLocationName=stateName}
        if (countyName != false){lowestLocationName=countyName}
    }
    return lowestLocationName;
}

// geolocation test stuff
var locationGranted; // declares global variable
var locationAutomaticURL; // declares the automatic 
var lowestLocationName; // 
function getLocationForButton(){
    getLocation();
    if (locationGranted){
        setMerchBox(generateImageID(countryCode,stateCode,countyName));
        console.log(locationAutomaticURL)
        console.log("yo")
    }
    if (locationAutomaticURL != undefined){
        x.innerHTML = lowestLocationName
    }
}

function handlePermission() {
    navigator.permissions.query({name:'geolocation'}).then(function(result) {
        console.log(result.state)
        if (result.state == 'granted') {
            locationGranted = true;
            getLocation();
        }
        else if (result.state == 'denied') {
            locationGranted = false;
        }
    });
}
// handlePermission()
      
var x = document.getElementById("b5");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    // x.innerHTML = lowestLocationName// "Latitude: " + position.coords.latitude +
    "<br>Longitude: " + position.coords.longitude;
    console.log("API called");
    fetch("https://api.mapbox.com/geocoding/v5/mapbox.places/"+position.coords.longitude+","+position.coords.latitude+".json?access_token=pk.eyJ1Ijoib3J0YW5hdGVjaCIsImEiOiJja3ZmZm1ycmYxeW1oMm5zMXV2b2FxbzRkIn0.GoeUfW-BSSY0K2xBpp_xdg").then(
        function(u){ return u.json();}).then(function(json){
            process_mapbox_geocode(json); // calling and passing json to another function process_mapbox_geocode
        }
    );

    // another functions
    function process_mapbox_geocode(data){
        document.cookie = "locationAutomaticURL=" + getRedirectURLMapbox(data.features[0]);
        locationGranted = true;
        if (locationGranted){
            console.log("changed click function");
            document.getElementById("b5").onclick = getRedirectURLMapbox(data.features[0]);
        }
    }
}

var input = document.getElementById('autocomplete');
var autocomplete = new google.maps.places.Autocomplete(input,{types: ["(regions)"], fields: ['address_components','adr_address','formatted_address']});
google.maps.event.addListener(autocomplete, 'place_changed', function(){
    var place = autocomplete.getPlace();

    var countyName = getCountry(place.address_components,"administrative_area_level_2");
    var stateCode = getCountry(place.address_components,"administrative_area_level_1");
    var countryCode = getCountry(place.address_components,"country");

    //  extract country short name (e.g. GB for Great Britain) from google geocode API result
    function getCountry(addrComponents,locality) {
        for (var i = 0; i < addrComponents.length; i++) {
            if (addrComponents[i].types[0] == locality) {
                return addrComponents[i].short_name;
            }
            if (addrComponents[i].types.length == 2) {
                if (addrComponents[i].types[0] == "political") {
                    return addrComponents[i].short_name;
                }
            }
        }
        return false;
    }

    console.log(getCountry(place.address_components,"country"));// gets country
    console.log(getCountry(place.address_components,"administrative_area_level_1"));// gets state
    console.log(getCountry(place.address_components,"administrative_area_level_2"));// gets county
    console.log(getCountry(place.address_components,"locality"));// gets locality

    // window.location.href = generateURL(countryCode,stateCode,countyName);
    imageID = generateImageID(countryCode,stateCode,countyName);
    console.log(imageID);
    setMerchBox(imageID, countryCode, generateURL(countryCode,stateCode,countyName));
}) 

function zazzleClicked(element) {
    if (element.includes("Product")) {
        let listId = element.charAt(element.length-1)-1
        element = PRODUCT_NAMES[listId] + " " + PRODUCT_IDS[listId];
    }
    console.log(element)
    gtag('event', "Zazzle Link Clicked", {
  'event_category': "commerce",
  'event_label': element,
  'value': "5"});
  
    twttr.conversion.trackPid('o7aq1', { tw_sale_amount: 0, tw_order_quantity: 0 });
    fbq('track', 'Purchase', {currency: "USD", value: 30.00});
    
};

$.get('https://www.cloudflare.com/cdn-cgi/trace', function(data) {
  // Convert key-value pairs to JSON
  // https://stackoverflow.com/a/39284735/452587
  data = data.trim().split('\n').reduce(function(obj, pair) {
    pair = pair.split('=');
    return obj[pair[0]] = pair[1], obj;
  }, {});
  sendESAnalytics(data.ip);
});

function sendESAnalytics(ip){
    var URL = 'https://u4ymsuodri7ngwgi5n4tjprgcq0qoeic.lambda-url.us-east-2.on.aws/'
    if (getCookie('_ga') != ""){
        URL += '?ga_id=' + getCookie('_ga') + '_' + ES_ID
    } else {
        URL += '?ga_id=' + encodeURIComponent('_' + ES_ID)
    }
    URL += '&user_agent=' + encodeURIComponent(navigator.userAgent)
    URL += '&ip=' + ip
    console.log("ip: " + ip)
    URL += '&fbp=' + fbp
    URL += '&twclid=' + twclid
    URL += '&timestamp_unix=' + new Date().getTime()
    URL += '&image_id=' + encodeURIComponent(globalImageID)

    fetch(URL)
    .then(function (u) {return u.json();})
    .then(function (json) {
    console.log(json); // calling and passing json to another function processPriceInfo
    });
}

const LANG = navigator.language;
countryLang = LANG.slice(LANG.length-2).toUpperCase();
console.log(countryLang);

// gets url parameters from url
var state = URL_PARAMS.get('state');
var county = URL_PARAMS.get('county');
var country = URL_PARAMS.get('country');
var loc = URL_PARAMS.get('location');

// if url parameters are present, set merch box to those values
if (loc){
    setMerchBox("location/"+loc, loc, generateURL(null,null,null,loc));
} else if (country || (state && country) || (county && state && country)) {
    setMerchBox(generateImageID(country,state,county), county ? county : state ? state : country, generateURL(country,state,county));
} else if (countryLang) {
    setMerchBox(countryLang,countryLang,generateURL(countryLang,null,null));
} else {
    setMerchBox("US", "United States","https://www.earthstripes.org/result/?country=US");
}