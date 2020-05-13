import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:lets_head_out/Screens/AddPlantPage.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:http/http.dart' as http;

import 'OverViewScreen.dart';

class Dashboard extends StatefulWidget {
  @override
  _DashboardState createState() => _DashboardState();
}

// PlantsList - parses list of json of plant data list
class PlantsList {
  final List<Plant> plants;

  PlantsList({
    this.plants,
  });

  factory PlantsList.fromJson(List<dynamic> parsedJson) {
    List<Plant> plants = new List<Plant>();
    plants = parsedJson.map((plantJson) => Plant.fromJson(plantJson)).toList();

    return new PlantsList(plants: plants);
  }
}

// Plant - parses individual json of plant map (dict)
class Plant {
  // setting variables
  final int currPhoto;
  final String dateCreated;
  final int plantId;
  final String plantName;
  final String species;
  final String uri;
  final String userEmail;

  // constructor
  Plant(
      {this.currPhoto,
      this.dateCreated,
      this.plantId,
      this.plantName,
      this.species,
      this.uri,
      this.userEmail});

  factory Plant.fromJson(Map<String, dynamic> json) {
    return Plant(
      currPhoto: json['curr_photo'],
      dateCreated: json['date_created'],
      plantId: json['plant_id'],
      plantName: json['plant_name'],
      species: json['species'],
      uri: json['uri'],
      userEmail: json['user_email'],
    );
  }
}

// fetchPlantsList - fetches list of all plants from http://localhost:5000/plants/
Future<PlantsList> fetchPlantsList() async {
  final String email = 'janesmith.synthesis@gmail.com/';
  // final response = await http.get('http://localhost:5000/plants/all/${email}');
  final response = await http.get(
      'http://backend-dev222222.us-east-1.elasticbeanstalk.com/plants/all/${email}');

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return PlantsList.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load plants list');
  }
}

class _DashboardState extends State<Dashboard> {
  Future<PlantsList> futurePlantsList;
  @override
  void initState() {
    super.initState();
    futurePlantsList = fetchPlantsList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            // ImageContainer(),
            Center(
              child: Column(children: <Widget>[
                SizedBox(
                  height: 50,
                ),
                Padding(
                  padding: const EdgeInsets.only(bottom: 20.0),
                  child: Align(
                      alignment: Alignment.center,
                      child: BoldText("My Plants", 20.0, kblack)),
                ),
                // FutureBuilder - used to fetch data
                FutureBuilder<PlantsList>(
                  future: futurePlantsList,
                  builder: (context, snapshot) {
                    // data good
                    if (snapshot.hasData) {
                      int numPlants = snapshot
                          .data.plants.length; // returns length of plants array
                      List<Widget> plantsRender = new List<
                          Widget>(); // creates new List<Widget> to add plants to for render
                      for (var i = 0; i < numPlants; i++) {
                        plantsRender.add(
                          buildContainer(
                              snapshot.data.plants[i].plantId,
                              snapshot.data.plants[i].plantName,
                              snapshot.data.plants[i].species,
                              snapshot.data.plants[i].userEmail,
                              snapshot.data.plants[i].dateCreated,
                              snapshot.data.plants[i].uri),
                        );
                        plantsRender.add(SizedBox(
                          height: 20.0,
                        ));
                      }
                      plantsRender.add(SizedBox(
                        height: 20.0,
                      ));
                      plantsRender
                          .add(SmallButtonGrey.bold("+ Add new plant", () {
                        Navigator.push(context,
                            new MaterialPageRoute(builder: (_) {
                          return AddPlantPage(email: 'janesmith.synthesis@gmail.com/');
                        }));
                      }, true));
                      // Adding extra spacing at the end so that scrolling works properly
                      plantsRender.add(SizedBox(
                        height: 200.0,
                      ));
                      // render
                      return Container(
                        width: MediaQuery.of(context).size.width,
                        height: MediaQuery.of(context).size.height,
                        decoration: BoxDecoration(
                            image: new DecorationImage(
                                image: new AssetImage(
                                    "assets/bgimg_dashboard.jpg"),
                                fit: BoxFit.cover),
                            color: Colors.grey.shade50,
                            borderRadius: BorderRadius.circular(15.0)),
                        child: ListView(
                          scrollDirection: Axis.vertical,
                          children: plantsRender,
                        ),
                      );
                    }
                    // error
                    else if (snapshot.hasError) {
                      return Text("${snapshot.error}");
                    }
                    // By default, show a loading spinner.
                    return CircularProgressIndicator();
                  },
                ),
              ]),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildContainer(id, name, species, email, date, uri) {
    return GestureDetector(
      onTap: () {
        Navigator.push(context, MaterialPageRoute(builder: (_) {
          return OverViewPage(plantId: id);
        }));
      },
      child: Container(
        width: 250,
        height: 100,
        child: Container(
            width: 250,
            height: 100,
            decoration: BoxDecoration(
              color: Colors.grey.shade50,
              borderRadius: BorderRadius.circular(15.0),
              border: Border.all(width: 2.0, color: Colors.black),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                Container(
                  width: 100,
                  height: 100,
                  child: ClipRRect(
                    borderRadius: new BorderRadius.only(
                        topLeft: Radius.circular(15),
                        bottomLeft: Radius.circular(15)),
                    child: Image.network(
                      uri,
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                SizedBox(
                  width: 10.0,
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    BoldText(name, 20.5, kblack),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: <Widget>[
                        Icon(
                          Icons.local_florist,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        BoldText("Species: " + species, 15.0, Colors.green),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.email,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        NormalText(email, kgreyDark, 11.0),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.perm_identity,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        NormalText(date, kgreyDark, 11.0),
                      ],
                    ),
                  ],
                )
              ],
            )),
      ),
    );
  }
}
