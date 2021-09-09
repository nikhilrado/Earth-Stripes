label.innerText = country + "  › ";
label.href = "?country=" + country;
label2.innerText = state;
label2.href = "?country=" + country + "&state=" + state;

//this operates the buttons that switch from Stripes to Bars
function switchStripes(switchTo) {
  if (switchTo == 'stripes'){
  document.getElementById('image1').src = "https://ortana-test.s3.us-east-2.amazonaws.com/v2/stripes/"+imageID+'.png';
  }
  if (switchTo == 'bars'){
  document.getElementById('image1').src = "https://ortana-test.s3.us-east-2.amazonaws.com/v2/labeled-bars/"+imageID+'.png';
  }
}

var data = "";
//fetch function
fetch(
"https://ortana-test.s3.us-east-2.amazonaws.com/json/" + imageID + ".json"
)
.then(function (u) {
return u.json();
})
.then(function (json) {
data_function(json); //calling and passing json to another function data_function
});

//sets the bars for yale data_function
function setYaleBars() {
YaleSubHeader.innerText =
"How people in " +
data["YaleClimateOpinionData2020"]["data"]["GeoName"] +
" view climate change";
datas = ["happening", "personal", "congress"];
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

//another functions
function data_function(jsonData) {
data = jsonData;

var encodedImageID = encodeURI(
"https://ortana-test.s3.us-east-2.amazonaws.com/v2/labeled-stripes/" +
  imageID +
  ".png"
);


//alert(data.sentence);
locationName = data.metadata.name;

myHeader9.innerText = locationName;
document.title = locationName + " - Earth Stripes";

startYear = data.resources.stripes["startYear"];
endYear = data.resources.stripes["endYear"];
description1 =
"This chart shows how climate change has affected " +
locationName +
" from " +
startYear +
"-" +
endYear +
", red stripes indicate warmer, and blue indicate lower temperatures.";
img1description.innerText = description1;

//yale information
setYaleBars();

merchLabel = encodedImageID + "&t_location_txt=" + locationName + " " + startYear + "-" + endYear
testmerchlink.href =
"https://www.zazzle.com/api/create/at-238391408801122257?rf=238391408801122257&ax=DesignBlast&sr=250403062909979961&cg=196064354850369877&t__useQpc=false&t__smart=false&tc=&ic=&t_labeledstripes_iid=" +
encodedImageID +
"&t_stripes_iid=" + merchLabel;

//deals with local impacts
if (country == "US" && state.length == 2) {
function combineParagraphs(index) {
  text = "";
  for (i = 0; i < data["local impacts"][index]["content"].length; i++) {
    text = text + data["local impacts"][index]["content"][i] + "\n\n";
    //console.log(text)
  }
  return text;
}

//set the names of all of the stuff
for (k = 0; k < data["local impacts"].length; k++) {
  element = document.getElementById("ImpactText" + (k + 1));
  element.innerText = combineParagraphs(k);
  element = document.getElementById("ImpactHeader" + (k + 1));
  element.innerText = data["local impacts"][k]["headline"];
  element = document.getElementById("ImpactPhoto" + (k + 1));
}

for (k = 0; k < data["local impacts"].length; k++) {
element = document.getElementById("ImpactPhoto" + (k + 1));
element.src = 'https://ortana-test.s3.us-east-2.amazonaws.com/photos/local-impact-photos/'+state+'/' + data["local impacts"][k]["img"]["file"] + ".jpg";
element.alt = data["local impacts"][k]["img"]["alt"]
element = document.getElementById("ImpactPhotoCaption" + (k + 1));
element.innerText = data["local impacts"][k]["img"]["caption"] + " Credit: " + data["local impacts"][k]["img"]["credit"] ;
}



//hide empty ones
console.log(8 - data["local impacts"].length);
for (k = 0; k < 8 - data["local impacts"].length; k++) {
  var box = document.getElementById("LocalImpactBox" + (8 - k));
  console.log("LocalImpactBox" + (8 - k));
  box.style.display = "none";
}
} else {
ImpactBox.style.display = "none";
}

function getSenatorInfo() {
//https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyB6RdsMva-gOY7FNxgrrHsBgskpF_a8njc&address=1263%20Pacific%20Ave.%20Kansas%20City%20KS
//AIzaSyB6RdsMva-gOY7FNxgrrHsBgskpF_a8njc

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
    
    senator1json = data["SenatorInfo"][json.officials[0].name]
    SenatorName1.innerText = json.officials[0].name;
    SenatorSubHeading1.innerText = "Senator, " + senator1json["stateName"] + ", " + senator1json["current term readable"] + " term";
    SenatorScore1.innerText = "Overall Score: " + senator1json["overallScore"];
    SenatorSite1txt.innerText = json.officials[0]["urls"][0].replace('https://www.','').replace('/','');
    SenatorSite1.href = json.officials[0]["urls"][0];

    senator2json = data["SenatorInfo"][json.officials[1].name]
    SenatorName2.innerText = json.officials[1].name;
    SenatorSubHeading2.innerText = "Senator, " + senator2json["stateName"] + ", " + senator2json["current term readable"] + " term";
    SenatorScore2.innerText = "Overall Score: " + senator2json["overallScore"];
    SenatorSite2txt.innerText = json.officials[1]["urls"][0].replace('https://www.','').replace('/','');
    SenatorSite2.href = json.officials[1]["urls"][0];
    
  console.log(JSON.stringify(json));
    //runs the images after in case there are any issues
    //SenatorImage2.src = json.officials[1].photoUrl  //photo from database
    SenatorImage2.src =
      "https://ortana-test.s3.us-east-2.amazonaws.com/senators/" +
      data["SenatorInfo"][json.officials[1].name]["image"];
    //SenatorImage1.src = json.officials[0].photoUrl //photo from database
    SenatorImage1.src =
      "https://ortana-test.s3.us-east-2.amazonaws.com/senators/" +
      data["SenatorInfo"][json.officials[0].name]["image"];

    console.log(
      "https://ortana-test.s3.us-east-2.amazonaws.com/senators/" +
        data["SenatorInfo"][json.officials[0].name]["image"]
    );
  });
}

getSenatorInfo();
}