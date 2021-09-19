const bucketPrefix = "https://ortana-test.s3.us-east-2.amazonaws.com/v2/"

//data acquired from query params that doesn't require json file
const urlParams = new URLSearchParams(window.location.search);
var state = urlParams.get('state');
var county = urlParams.get('county');
var country = urlParams.get('country');

const countriesWithStates = ['AU','BR','CA','CN','IN','RU','US']
if (countriesWithStates.includes(country)){
if (!(county == null || county == "false")) {
    county = county.replace(/ /g, "+")
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
document.getElementById('image1').src = "https://ortana-test.s3.us-east-2.amazonaws.com/v2/stripes/" + imageID+'.png';

label.innerText = country + "  › ";
label.href = "?country=" + country;
label2.innerText = state;
label2.href = "?country=" + country + "&state=" + state;

var encodedImageID = encodeURI(
    bucketPrefix + "labeled-stripes/" + imageID + ".png"
);

//this operates the buttons that switch from Stripes to Bars
function switchStripes(switchTo) {
    if (switchTo == 'stripes'){
    document.getElementById('image1').src = bucketPrefix + "stripes/" + imageID + '.png';
    }
    if (switchTo == 'bars'){
    document.getElementById('image1').src = bucketPrefix + "labeled-bars/"+imageID+'.png';
    }
}

//fetches the smallest location json file
var data = "";
fetch(bucketPrefix + "json/" + imageID + ".json")
.then(function (u) {return u.json();})
.then(function (json) {
  data_function(json); //calling and passing json to another function data_function
});

//deals with local impacts
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

        //set the names of all of the stuff
        for (k = 0; k < data.length; k++) {
            element = document.getElementById("ImpactText" + (k + 1));
            element.innerText = combineParagraphs(k);
            element = document.getElementById("ImpactHeader" + (k + 1));
            element.innerText = data[k]["headline"];
            element = document.getElementById("ImpactPhoto" + (k + 1));
        }
        
        //loop through each impact, if there isn't a photo, hide it, if there is, retrieve it and insert alt text
        for (k = 0; k < data.length; k++) {
        element = document.getElementById("ImpactPhoto" + (k + 1));
                console.log(data[k]["img"]["file"])
            if (data[k]["img"]["file"] == null || data[k]["img"]["file"] == ""){
                element.style.display = "none";
            }
            else {
                element.src = bucketPrefix + 'photos/local-impact-photos/'+state+'/' + data[k]["img"]["file"] + ".jpg";
                element.alt = data[k]["img"]["alt"];
            }
        
        //if there isn't a caption hide it, if there is fill in the data and credit
        element = document.getElementById("ImpactPhotoCaption" + (k + 1));
        if (data[k]["img"]["caption"] == null ){
                element.style.display = "none";
            }
            else {
                element.innerText = data[k]["img"]["caption"] + " Credit: " + data[k]["img"]["credit"] ;
            }
        
        }
        
        //hide empty local impact data boxes
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

//sets the bars for yale data_function
function setYaleBars() {
    YaleSubHeader.innerText = "How people in " + data["YaleClimateOpinionData2020"]["data"]["GeoName"] + " view climate change";
    datas = ["happening", "personal", "congress","fundrenewables"];

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

function setMerchBox(){
merchLabel = encodedImageID + "&t_location_txt=" + locationName + " " + startYear + "-" + endYear;
customMerchLink = "https://www.zazzle.com/api/create/at-238391408801122257?rf=238391408801122257&ax=DesignBlast&sr=250403062909979961&cg=196064354850369877&t__useQpc=false&t__smart=false&tc=&ic=&t_labeledstripes_iid="
+ encodedImageID + "&t_stripes_iid=" + merchLabel;
testmerchlink.href = customMerchLink;

productNames = ["Magnet","Mug","Tie","Stickers"]
productIDs = ['147662722592724730','168540946485519042','151119561160107608','217917661479101292']
for (i=1; i<=productNames.length; i++){
element = document.getElementById('ProductImage' + i);
var imageID2 = 'https://rlv.zazzle.com/svc/view?pid='+productIDs[i-1]+'&max_dim=600&at=238391408801122257&t_stripes_url='+encodedImageID + '&t_stripes2_url='+encodedImageID;
element.src = imageID2;
element.alt = "warming stripes " + productNames[i-1]
element = document.getElementById('ProductName' + i);
element.innerText = productNames[i-1];
element = document.getElementById('Product'+i+"Link");
element.href = customMerchLink;
element = document.getElementById('Product'+i+'Link2');
element.href = customMerchLink;
console.log("product round "  + i);
}
}

function getSenatorInfo(senatorData) { 
  //fetch function
  fetch(
    "https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyB6RdsMva-gOY7FNxgrrHsBgskpF_a8njc&levels=country&roles=legislatorUpperBody&address=" +
      state +
      ",USA"
  )
    .then(function (u) {
      return u.json();
    })
    .then(function (json) {
      //data_function(json); //calling and passing json to another function data_function
      console.log(json);
      
      senator1json = senatorData[json.officials[0].name]
      SenatorName1.innerText = json.officials[0].name;
      SenatorSubHeading1.innerText = "Senator, " + senator1json["stateName"] + ", " + senator1json["current term readable"] + " term";
      SenatorScore1.innerText = "Overall Score: " + senator1json["overallScore"];
      SenatorSite1txt.innerText = json.officials[0]["urls"][0].replace('https://www.','').replace('/','');
      SenatorSite1.href = json.officials[0]["urls"][0];

      senator2json = senatorData[json.officials[1].name]
      SenatorName2.innerText = json.officials[1].name;
      SenatorSubHeading2.innerText = "Senator, " + senator2json["stateName"] + ", " + senator2json["current term readable"] + " term";
      SenatorScore2.innerText = "Overall Score: " + senator2json["overallScore"];
      SenatorSite2txt.innerText = json.officials[1]["urls"][0].replace('https://www.','').replace('/','');
      SenatorSite2.href = json.officials[1]["urls"][0];
      
    console.log(JSON.stringify(json));
      //runs the images after in case there are any issues
      //SenatorImage2.src = json.officials[1].photoUrl  //photo from database
      SenatorImage2.src = bucketPrefix + "photos/senators/" + senatorData[json.officials[1].name]["image"];
      //SenatorImage1.src = json.officials[0].photoUrl //photo from database
      SenatorImage1.src = bucketPrefix + "photos/senators/" + senatorData[json.officials[0].name]["image"];

      console.log(bucketPrefix + "senators/" + senatorData[json.officials[0].name]["image"]
      );
    });
}


function handleStateJSON(json){
    setLocalImpacts(json["local impacts"]);
    getSenatorInfo(json["SenatorInfo"]);
}

if (country == "US" && typeof state == "string"){
    getSenatorInfo();
} else {
    legislativeBox.style.display = "none";
}

//main function that loads JSON data
function data_function(jsonData) {
console.log(jsonData)
//if there is a county (hence in US) and there are no local impacts data for the county, fetch the state data
if (typeof county == "string" && jsonData["local impacts"] == null){
    fetch(bucketPrefix + "json/" + country + "/" + state + ".json")
    .then(function (u) {return u.json();})
    .then(function (json) {
      handleStateJSON(json); //calling and passing json to another function data_function
    });
} else {
    setLocalImpacts(jsonData["local impacts"]);
    getSenatorInfo(jsonData["SenatorInfo"]);

}
data = jsonData;

//alert(data.sentence);
locationName = data.metadata.name;

myHeader9.innerText = locationName;
//document.title = locationName + " - Earth Stripes"; //changed the title but now we use php

startYear = data.resources.stripes["startYear"];
endYear = data.resources.stripes["endYear"];
description1 = "These warming stripes show how climate change has affected " + locationName + " from " + startYear + "-" + endYear + ", red stripes indicate warmer, and blue indicate lower temperatures.";
img1description.innerText = description1;

//yale information
try{
setYaleBars();
}catch (error) {
    console.warn("No Yale Climate Opinion Data Found");
    YaleOpinion.style.display = "none";
}

setMerchBox();

}