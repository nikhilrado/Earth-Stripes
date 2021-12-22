//document.getElementById("autocomplete").focus();

var changeLocationBoxIsHidden = true;
function toggleChangeLocation(action=null){
    var element = document.getElementById("changeLocationBox");
    if(changeLocationBoxIsHidden && action!="hide"){
        element.style.display = "block";
        changeLocationBoxIsHidden = false;
    }
    else{
        element.style.display = "none";
        changeLocationBoxIsHidden = true;
    }
    console.log(changeLocationBoxIsHidden)
}

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

const countriesWithStates = ['AU','BR','CA','CN','IN','RU','US']
function generateImageID (countryCode=null, stateCode=null, countyName=null){
    var ImageID = countryCode

    if (countriesWithStates.includes(countryCode)) {
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
const productNames = ["Cloth Mask","Mug","Tie","Stickers", "Magnet","Badge (Pin)", "T-Shirt", "Socks"];
const productIDs = ['256670743725195335','168540946485519042','151119561160107608','217917661479101292','147753984968275362', '145354997245092652', '235484093576644423','256547457460896288'];
function setMerchBox(imageID, locationName, locationURL){
    var encodedLabeledStripesImageURL = encodeURI(bucketPrefix + "labeled-stripes/" + imageID + ".png?request=zazzle");
    console.log(bucketPrefix + "labeled-stripes/" + imageID + ".png?request=zazzle");
    var encodedStripesImageURL = encodeURI(bucketPrefix + "stripes/" + imageID + ".png?request=zazzle");
    
    merchLabel = "&t_location_txt=" + encodeURIComponent(locationName);// + " " + startYear + "-" + endYear);
    customMerchLink = "https://www.zazzle.com/api/create/at-238391408801122257?rf=238391408801122257&ax=DesignBlast&sr=250403062909979961&cg=196064354850369877&t__useQpc=false&t__smart=false&t_labeledstripes_iid="
    + encodedLabeledStripesImageURL + "&tc=merch-page&ic=" + imageID.replace(/[^a-zA-z]/g,'_') + "&t_stripes_iid=" + encodedStripesImageURL + merchLabel;
    //testmerchlink.href = customMerchLink;
    MerchButton.href = customMerchLink;
    console.log(imageID.replace(/[^a-zA-z]/g,'_'));
    
    for (i=1; i<=productNames.length; i++){
        element = document.getElementById('ProductImage' + i);
        var imageID2 = 'https://rlv.zazzle.com/svc/view?pid='+productIDs[i-1]+'&max_dim=600&at=238391408801122257&t_stripes_url='+encodedStripesImageURL + '&t_labeledstripes_url='+encodedLabeledStripesImageURL;
        element.src = imageID2;
        element.alt = "Warming Stripes " + productNames[i-1];
        element = document.getElementById('ProductName' + i);
        element.innerText = productNames[i-1];
        element = document.getElementById('Product'+i+"Link");
        element.href = customMerchLink;
        element = document.getElementById('Product'+i+'Link2');
        element.href = customMerchLink;
    }
    
    element = document.getElementById('locationName');
    element.innerText = imageID.replaceAll("+"," ");
    element = document.getElementById('locationNameLink');
    console.log(locationAutomaticURL);
    element.href = locationAutomaticURL;
    

    var yeet = document.getElementById("underline-text");
    myArray= imageID.split("/");
    locationName = myArray[myArray.length - 1].replaceAll("+"," ")
    countryCode = myArray[0]
    if (countryCode == locationName && locationName.length == 2){ //if it is just a country code, replace with name
        locationName = getCountryFromCountryCode(locationName);
    }
    yeet.textContent = locationName;
    toggleChangeLocation(action="hide");
} 

//custom function to get Redirect URL
function getRedirectURLMapbox(jsonPlaceData,redirectNow=false) {
    placeName = jsonPlaceData.place_name
    
    //gets the country code of location
    if (jsonPlaceData.place_type[0]=="country"){
        countryCode = jsonPlaceData.properties.short_code
        countryName = jsonPlaceData.text
    }
    else {
        countryCode = jsonPlaceData.context[jsonPlaceData.context.length-1].short_code
        countryName = jsonPlaceData.context[jsonPlaceData.context.length-1].text
    }
    countryCode = countryCode.toUpperCase()
    
    //get stateCode
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
    
    //get county
    if (jsonPlaceData.place_type[0]=="district"){
        countyName = jsonPlaceData.text
        console.log("rancty")
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
        //window.location.href = locationAutomaticURL
    }

    x.innerHTML = lowestLocationName
    return locationAutomaticURL; 
}

function getLowestLocationName(countryCode,stateCode,countyName){
    //get lowest location name which will be used as the label for the location btn
    lowestLocationName = countryName
    //tried to insert this stuff next to if statement to run when country is just US
    if (countryCode != "US"){
        lowestLocationName = countryName //sets it to country name if not US
    }
    else{
        if (stateCode != false){lowestLocationName=stateName}
        if (countyName != false){lowestLocationName=countyName}
    }
    return lowestLocationName;
}

//geolocation test stuff
var locationGranted; //declares global variable
var locationAutomaticURL; //declares the automatic 
var lowestLocationName; //
function getLocationForButton(){
    getLocation();
    if (locationGranted){
        //window.location.href = locationAutomaticURL
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
        console.log("yehaw")
        console.log(result.state)
        if (result.state == 'granted') {
            console.log("yehaw")
            locationGranted = true;
            getLocation();
        }
        else if (result.state == 'denied') {
            locationGranted = false;
        }
    });
}
handlePermission()
      
var x = document.getElementById("b5");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    //x.innerHTML = lowestLocationName//"Latitude: " + position.coords.latitude +
    "<br>Longitude: " + position.coords.longitude;
    console.log("API called");
    fetch("https://api.mapbox.com/geocoding/v5/mapbox.places/"+position.coords.longitude+","+position.coords.latitude+".json?access_token=pk.eyJ1Ijoib3J0YW5hdGVjaCIsImEiOiJja3ZmZm1ycmYxeW1oMm5zMXV2b2FxbzRkIn0.GoeUfW-BSSY0K2xBpp_xdg").then(
        function(u){ return u.json();}).then(function(json){
            process_mapbox_geocode(json); //calling and passing json to another function process_mapbox_geocode
        }
    );

    //another functions
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

    // extract country short name (e.g. GB for Great Britain) from google geocode API result
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

    console.log(getCountry(place.address_components,"country"));//gets country
    console.log(getCountry(place.address_components,"administrative_area_level_1"));//gets state
    console.log(getCountry(place.address_components,"administrative_area_level_2"));//gets county
    console.log(getCountry(place.address_components,"locality"));//gets locality

    //window.location.href = generateURL(countryCode,stateCode,countyName);
    imageID = generateImageID(countryCode,stateCode,countyName);
    console.log(imageID);
    setMerchBox(imageID, countryCode, generateURL(countryCode,stateCode,countyName));
}) 

setMerchBox("US", "United States");  
const lang = navigator.language;
countryLang = lang.substr(lang.length-2).toUpperCase();
console.log(countryLang);
setMerchBox(countryLang,countryLang,generateURL(countryLang,null,null));