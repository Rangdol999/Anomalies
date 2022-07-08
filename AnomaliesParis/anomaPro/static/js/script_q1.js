console.log("hello ji")

function initMap() {
  // carte centrÃ©e sur Paris : 
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 48.856615, lng: 2.342324 },
    zoom: 12,
  });

 
  var ctx = document.getElementById('map')
  const data_to_map = JSON.parse(ctx.dataset.my_data)
  //var data_to_map = ctx.dataset.my_data
  console.log(data_to_map)

  arrondissements = {1:{ lat: 48.863221, lng: 2.335483 },2:{lat: 48.868620, lng: 2.341882},3:{lat:48.863154, lng: 2.360451}}

  for (let year in data_to_map){
    // console.log(data_to_map[year])
    for (let arr in data_to_map[year]){
      console.log(data_to_map[year][arr])
      
      new google.maps.Circle({
        center : arrondissements[arr],
        map: map,
        radius : data_to_map[year][arr],
      })
    }
  }
} 
 