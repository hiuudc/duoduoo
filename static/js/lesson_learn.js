// // const xhr = new XMLHttpRequest();
// // const method = 'POST';
// // const url = lessonURL;
// // const responseType = "json";
// // var data = {
// //     "words": [
// //         { "word_id": 1, "point": 0.2 },
// //         { "word_id": 2, "point": 0.2 },
// //         { "word_id": 3, "point": 0.2 }
// //     ]
// // };
// // xhr.responseType = responseType;
// // xhr.open(method, url);
// // xhr.setRequestHeader()
// // xhr.onload = function () {
// //     // const serverResponse = xhr.response
// //     // const data = serverResponse.response
// // };
// // xhr.send(data);

// /*
// This code originated with Steven Estrella of ShearSpire Media. Please retain this comment if you fork this pen. The original pen can be found at:
// https://codepen.io/sgestrella/pen/QodzgY
// */
// let allVoices, allLanguages, primaryLanguages, langtags, langhash, langcodehash;
// let txtFld, rateFld, speakBtn, speakerMenu, languageMenu, blurbs;
// let voiceIndex = 0;
// let initialSetup = true;
// let defaultBlurb = "I enjoy the traditional music of my native country.";


// function init(){
//   speakBtn = document.querySelector("#speakBtn");
//   txtFld = document.querySelector("#txtFld"); 
//   speakerMenu = document.querySelector("#speakerMenu");
//   langtags = getLanguageTags();
//   speakBtn.addEventListener("click",talk,false);
//   speakerMenu.addEventListener("change",selectSpeaker,false);
  
//   createBlurbs();
//   rateFld = document.querySelector("#rateFld");
//   languageMenu = document.querySelector("#languageMenu"); 
//   languageMenu.addEventListener("change",selectLanguage,false);
//   langhash = getLookupTable(langtags,"name");
//   langcodehash = getLookupTable(langtags,"code");
  
//   if (window.speechSynthesis) {
//     if (speechSynthesis.onvoiceschanged !== undefined) {
//       //Chrome gets the voices asynchronously so this is needed
//       speechSynthesis.onvoiceschanged = setUpVoices;
//     }
//     setUpVoices(); //for all the other browsers
//   }else{
//     speakBtn.disabled = true;
//     speakerMenu.disabled = true;
//     languageMenu.disabled = true;
//     document.querySelector("#warning").style.display = "block";
//   }
// }
// function setUpVoices(){
//   allVoices = getAllVoices();
//   allLanguages = getAllLanguages(allVoices);
//   primaryLanguages = getPrimaryLanguages(allLanguages);
//   filterVoices();
//   if (initialSetup && allVoices.length){
//     initialSetup = false;
//     createLanguageMenu();
//   }
// }
// function talk(){
//   let sval = Number(speakerMenu.value);
//   let u = new SpeechSynthesisUtterance();
//   u.voice = allVoices[sval];
//   u.lang = u.voice.lang;
//   u.text = txtFld.value;
//   u.rate = Number(rateFld.value);
//   speechSynthesis.speak(u);
// }
// function createLanguageMenu(){
//   let code = `<option selected value="all">Show All</option>`;
//   let langnames = [];
//   primaryLanguages.forEach(function(lobj,i){
//     langnames.push(langcodehash[lobj.substring(0,2)].name);
//   });
//   langnames.sort();
//   langnames.forEach(function(lname,i){
//     let lcode = langhash[lname].code;
//     code += `<option value=${lcode}>${lname}</option>`;
//   });
//   languageMenu.innerHTML = code;
// }
// function createSpeakerMenu(voices){
//   let code = ``;
//   voices.forEach(function(vobj,i){
//     code += `<option value=${vobj.id}>${vobj.name} (${vobj.lang})`;
//     code += vobj.voiceURI.includes(".premium") ? ' (premium)' : ``;
//     code += `</option>`;
//   });
//   speakerMenu.innerHTML = code;
// }
// function getAllLanguages(voices){
//   let langs = [];
//   voices.forEach(vobj => {
//     langs.push(vobj.lang.trim());
//   });
//   return [...new Set(langs)];
// }
// function  getPrimaryLanguages(langlist){
//   let langs = [];
//   langlist.forEach(vobj => {
//     langs.push(vobj.substring(0,2));
//   });
//   return [...new Set(langs)];
// }
// function selectSpeaker(){
//   voiceIndex = speakerMenu.selectedIndex;
// }
// function selectLanguage(){
//   filterVoices();
//   speakerMenu.selectedIndex = 0;
// }
// function filterVoices(){
//   let langcode = languageMenu.value;
//   voices = allVoices.filter(function (voice) {
//     return langcode === "all" ? true : voice.lang.indexOf(langcode + "-") >= 0;
//   });
//   createSpeakerMenu(voices);
//   let t = blurbs[languageMenu.options[languageMenu.selectedIndex].text];
//   txtFld.value = t ? t : defaultBlurb;
//   speakerMenu.selectedIndex = voiceIndex;
// }


// function getAllVoices() {
//   let voicesall = speechSynthesis.getVoices();
//   let vuris = [];
//   let voices = [];
//   //unfortunately we have to check for duplicates
//   voicesall.forEach(function(obj,index){
//     let uri = obj.voiceURI;
//     if (!vuris.includes(uri)){
//         vuris.push(uri);
//         voices.push(obj);
//      }
//   });
//   voices.forEach(function(obj,index){obj.id = index;});
//   return voices;
// }
// function createBlurbs(){
//   blurbs = {
//     "Arabic" : "?????? ???????????? ?????????????????? ?????????????????? ?????????? ????????.",
//     "Chinese" : "????????????????????????????????????",
//     "Czech" : "M??m r??d tradi??n?? hudbu m?? rodn?? zem??.",
//     "Danish" : "Jeg nyder den traditionelle musik i mit hjemland.",
//     "Dutch" : "Ik geniet van de traditionele muziek van mijn geboorteland.",
//     "English" : "I enjoy the traditional music of my native country.",
//     "Finnish" : "Nautin kotimaassani perinteist?? musiikkia.",
//     "French" : "J'appr??cie la musique traditionnelle de mon pays d'origine.",
//     "German" : "Ich genie??e die traditionelle Musik meiner Heimat.",
//     "Greek" : "???????????????????? ?????? ?????????????????????? ?????????????? ?????? ???????????????? ??????.",
//     "Hebrew" : "?????? ???????? ???????????????? ???????????????? ???? ????????????.",
//     "Hindi" : "????????? ???????????? ????????? ????????? ?????? ???????????????????????? ??????????????? ?????? ???????????? ???????????? ????????????",
//     "Hungarian" : "??lvezem az ??n haz??m hagyom??nyos zen??j??t.",
//     "Indonesian" : "Saya menikmati musik tradisional negara asal saya.",
//     "Italian" : "Mi piace la musica tradizionale del mio paese natale.",
//     "Japanese" : "??????????????????????????????????????????????????????",
//     "Korean" : "?????? ??? ????????? ?????? ????????? ?????????.",
//     "Norwegian Bokmal" : "Jeg liker den tradisjonelle musikken i mitt hjemland.",
//     "Polish" : "Lubi?? tradycyjn?? muzyk?? mojego kraju.",
//     "Portuguese" : "Eu gosto da m??sica tradicional do meu pa??s natal.",
//     "Romanian" : "??mi place muzica tradi??ional?? din ??ara mea natal??.",
//     "Russian" : "?????? ???????????????? ???????????????????????? ???????????? ???????? ???????????? ????????????.",
//     "Slovak" : "M??m r??d tradi??n?? hudbu svojej rodnej krajiny.",
//     "Spanish" : "Disfruto de la m??sica tradicional de mi pa??s natal.",
//     "Swedish" : "Jag njuter av traditionell musik i mitt hemland.",
//     "Thai" : "????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
//     "Turkish" : "??lkemdeki geleneksel m??zikten zevk al??yorum."
//   };
// }
// function getLanguageTags(){
//   let langs = ["ar-Arabic","cs-Czech","da-Danish","de-German","el-Greek","en-English","eo-Esperanto","es-Spanish","et-Estonian","fi-Finnish","fr-French","he-Hebrew","hi-Hindi","hu-Hungarian","id-Indonesian","it-Italian","ja-Japanese","ko-Korean","la-Latin","lt-Lithuanian","lv-Latvian","nb-Norwegian Bokmal","nl-Dutch","nn-Norwegian Nynorsk","no-Norwegian","pl-Polish","pt-Portuguese","ro-Romanian","ru-Russian","sk-Slovak","sl-Slovenian","sq-Albanian","sr-Serbian","sv-Swedish","th-Thai","tr-Turkish","zh-Chinese"];
//   let langobjects = [];
//   for (let i=0;i<langs.length;i++){
//     let langparts = langs[i].split("-");
//     langobjects.push({"code":langparts[0],"name":langparts[1]});
//   }
//   return langobjects;
// }

// function getLookupTable(objectsArray,propname){
//   return objectsArray.reduce((accumulator, currentValue) => (accumulator[currentValue[propname]] = currentValue, accumulator),{});
// }
// document.addEventListener('DOMContentLoaded', function (e) {
//   try {init();} catch (error){
//     console.log("Data didn't load", error);}
// });