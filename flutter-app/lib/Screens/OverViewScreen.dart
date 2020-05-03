import 'dart:convert';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:http/http.dart' as http;

class OverViewPage extends StatefulWidget {
  final int plantId;
  OverViewPage({Key key, @required this.plantId}) : super(key: key);

  @override
  _OverViewPageState createState() => _OverViewPageState();
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
// end Plant

// PlantRequest - parses json to water plant through /requests in backend
class PlantRequest {
  final String plantId;
  final String timestamp;
  final String category;

  PlantRequest({
    this.plantId,
    this.timestamp,
    this.category,
  });

  factory PlantRequest.fromJson(Map<String, dynamic> json) {
    return PlantRequest(
      plantId: json['plant_id'],
      timestamp: json['timestamp'],
      category: json['category'],
    );
  }
}
// end WaterPlant

// fetchPlantsList - fetches list of all plants from http://localhost:5000/plants/
Future<Plant> fetchPlantInfo(id) async {
  final response = await http.get('http://localhost:5000/plants/plant/${id}');

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Plant.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load plant');
  }
}
// end fetchPlantInfo

// makeRequest - makes request to http://localhost:5000/requests/insert
Future<PlantRequest> makeRequest(
    String plantId, String timestamp, String category) async {
  final http.Response response = await http.post(
    'http://localhost:5000/requests/insert',
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      "plant_id": plantId,
      "timestamp": timestamp,
      "category": category,
    }),
  );
  if (response.statusCode == 200) {
    // If the server did return a 201 CREATED response,
    // then parse the JSON.
    return PlantRequest.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 201 CREATED response,
    // then throw an exception.
    throw Exception('Failed to load plant request');
  }
}
// end makeRequest

class _OverViewPageState extends State<OverViewPage>
    with SingleTickerProviderStateMixin {
  TabController tabController;
  Future<Plant> futurePlant;
  Future<PlantRequest> grabPicture;
  Future<PlantRequest> toggleLight;
  Future<PlantRequest> waterPlant;

  @override
  void initState() {
    super.initState();
    tabController = new TabController(length: 1, vsync: this);
    futurePlant = fetchPlantInfo(widget.plantId);
  }

  @override
  void dispose() {
    super.dispose();
    tabController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // backgroundColor: kwhite,
        body: Stack(children: <Widget>[
      Container(
        decoration: BoxDecoration(
            image: DecorationImage(
                image: AssetImage("assets/bgimg_overview.jpg"),
                fit: BoxFit.cover)),
        child: Scaffold(
            backgroundColor: Colors.transparent,
            appBar: AppBar(
              elevation: 0,
              backgroundColor: Colors.transparent,
            ),
            body: FutureBuilder<Plant>(
                future: futurePlant,
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return SingleChildScrollView(
                        // child: Center(
                        child: Align(
                            // alignment: Alignment.centerLeft,
                            child: Column(
                      children: <Widget>[
                        Image.asset(
                          "assets/orchid.jpg",
                          height: 200.0,
                          width: 200,
                          fit: BoxFit.fill,
                        ),
                        SizedBox(height: 20),
                        BoldText(
                            "Name: " + snapshot.data.plantName, 20, kblack),
                        SizedBox(height: 20),
                        BoldText(
                            "Species: " + snapshot.data.species, 20, kblack),
                        SizedBox(height: 20),
                        BoldText(
                            "Email: " + snapshot.data.userEmail, 20, kblack),
                        SizedBox(height: 20),
                        BoldText("Date created: " + snapshot.data.dateCreated,
                            20, kblack),
                        SizedBox(height: 160),
                        (grabPicture == null)
                            ? WideButtonBlue("Get Live Picture", () {
                                setState(() {
                                  grabPicture = makeRequest(
                                      widget.plantId.toString(), "", "picture");
                                });
                              })
                            : FutureBuilder<PlantRequest>(
                                future: grabPicture,
                                builder: (context, snapshot) {
                                  if (snapshot.hasData) {
                                    return Text(
                                        "Successfully captured picture!",
                                        style: TextStyle(
                                            backgroundColor: Colors.blue,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  } else if (snapshot.hasError) {
                                    return Text("${snapshot.error}",
                                        style: TextStyle(
                                            backgroundColor: Colors.red,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  }
                                  return CircularProgressIndicator();
                                },
                              ),
                        SizedBox(height: 20),
                        (toggleLight == null)
                            ? WideButtonYellow("Turn On Light", () {
                                setState(() {
                                  toggleLight = makeRequest(
                                      widget.plantId.toString(), "", "light");
                                });
                              })
                            : FutureBuilder<PlantRequest>(
                                future: toggleLight,
                                builder: (context, snapshot) {
                                  if (snapshot.hasData) {
                                    return Text("Successfully turned on light!",
                                        style: TextStyle(
                                            backgroundColor: Colors.orange,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  } else if (snapshot.hasError) {
                                    return Text("${snapshot.error}",
                                        style: TextStyle(
                                            backgroundColor: Colors.red,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  }
                                  return CircularProgressIndicator();
                                },
                              ),
                        SizedBox(height: 20),
                        (waterPlant == null)
                            ? WideButtonGreen("Water Plant", () {
                                setState(() {
                                  waterPlant = makeRequest(
                                      widget.plantId.toString(), "", "water");
                                });
                              })
                            : FutureBuilder<PlantRequest>(
                                future: waterPlant,
                                builder: (context, snapshot) {
                                  if (snapshot.hasData) {
                                    return Text("Successfully watered plant!",
                                        style: TextStyle(
                                            backgroundColor: Colors.green,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  } else if (snapshot.hasError) {
                                    return Text("${snapshot.error}",
                                        style: TextStyle(
                                            backgroundColor: Colors.red,
                                            fontSize: 30),
                                        textAlign: TextAlign.center);
                                  }
                                  return CircularProgressIndicator();
                                },
                              ),
                      ],
                    ))
                        // )
                        );
                  }
                  // error
                  else if (snapshot.hasError) {
                    return Text("${snapshot.error}",
                        style: TextStyle(
                            backgroundColor: Colors.red, fontSize: 30));
                  }
                  // By default, show a loading spinner.
                  return CircularProgressIndicator();
                })),
      )
    ]));
  }
}
