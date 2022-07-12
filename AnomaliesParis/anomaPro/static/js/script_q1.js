console.log("Question 1 niveau 0")

arrondissements = {
  1:{ lat: 48.863221, lng: 2.335483 },
  2:{lat: 48.868620, lng: 2.341882},
  3:{lat:48.863154, lng: 2.360451},
  4:{lat:48.8540842,lng:2.3393978},
  5:{lat:48.8453867,lng:2.3512436},
  6:{lat:48.8495441,lng:2.3131751},
  7:{lat:48.8548428,lng:2.3115698},
  8:{lat:48.8732249,lng:2.3111174},
  9:{lat:48.8770656,lng:2.3203167},
  10:{lat:48.8759748,lng:2.3448589},
  11:{lat:48.8600971,lng:2.3640365},
  12:{lat:48.8351684,lng:2.3821573},
  13:{lat:48.8304322,lng:2.3481861},
  14:{lat:48.8296054,lng:2.3054196},
  15:{lat:48.841768,lng:2.2588125},
  16:{lat:48.8557618,lng:2.2227713},
  17:{lat:48.887399,lng:2.2872137},
  18:{lat:48.8919861,lng:2.3311888},
  19:{lat:48.8871723,lng:2.3527476},
  20:{lat:48.8625523,lng:2.3616608},
}

function initMap() {
  console.log("function initMap!")
  // carte centrÃ©e sur Paris : 
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: lat_a, lng: long_a },
    zoom: 12,
  });

  console.log(data_to_map)

  for (let arr in data_to_map){
    //loop through ARRONDISSEMENTS

    new google.maps.Marker({
      position: arrondissements[arr],
      map: map,
      label: "Arr"+arr
    })

    for (let year in data_to_map[arr]){
      // loop through YEARS
      
      // define color based on YEAR
      if (year == 2022){
        var color_fill = "#e75c31" 
        var color_line = "#e75c31"
      }
      else if (year == 2021){
        var color_fill = "#41c5b8" 
        var color_line = "#41c5b8"
      }

      // put a circle which radius is linked to quantity, centered on the ARRONDISSEMENT
      new google.maps.Circle({
        center : arrondissements[arr],
        map: map,
        radius : data_to_map[arr][year]/100,
        strokeColor: color_line,
        StrokeOpacity: 0.8,
        fillColor: color_fill,
        fillOpacity: 0.5,
      })
    }
  }
} 
 





const imagesPie = document.querySelectorAll("#image_bg img")
const model = document.querySelector(".modelImage")
const fullImg = document.querySelector(".imgShow")

imagesPie.forEach(image => {
  image.addEventListener('click', ()=> {
    model.classList.add("open");

    fullImg.src = image.src
  })
})

model.addEventListener("click", e=> {
  if(e.target != this.target) {
    model.classList.remove("open");
  }
})




