import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:lets_head_out/Screens/DashBoard.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:lets_head_out/utils/forms.dart';
import 'package:http/http.dart' as http;

class UpdatePlantPage extends StatefulWidget {
  final int plantId;
  String plantName;
  String species;
  String userEmail;
  String uri;
  String serialPort;
  int position;
  int currPhoto;
  int waterThreshold;
  int lightThreshold;

  UpdatePlantPage({
    Key key,
    @required this.plantId,
    @required this.plantName,
    @required this.species,
    @required this.userEmail,
    @required this.uri,
    @required this.serialPort,
    @required this.position,
    @required this.currPhoto,
    @required this.waterThreshold,
    @required this.lightThreshold,
  }) : super(key: key);

  @override
  _UpdatePlantPageState createState() => _UpdatePlantPageState();
}

// PlantsList - parses list of json of plant data list
class UpdateList {
  List plants;

  UpdateList({
    this.plants,
  });

  factory UpdateList.fromJson(List<dynamic> parsedJson) {
    // PlantRequest plants = new PlantRequest();
    // // print(plants);
    // // print(parsedJson);
    // // print(parsedJson[1]);
    // plants = parsedJson;

    return new UpdateList(plants: parsedJson);
  }
}

// PlantRequest - parses json to water plant through /requests in backend
class PlantRequest {
  final String userEmail;
  final String plantName;
  final String species;
  final String serialPort;
  final int position;
  final int currPhoto;
  final int waterThreshold;
  final int lightThreshold;

  PlantRequest({
    this.userEmail,
    this.plantName,
    this.species,
    this.serialPort,
    this.position,
    this.currPhoto,
    this.waterThreshold,
    this.lightThreshold,
  });

  factory PlantRequest.fromJson(Map<String, dynamic> json) {
    return PlantRequest(
      userEmail: json['user_email'],
      plantName: json['plant_name'],
      species: json['species'],
      serialPort: json['serial_port'],
      position: json['position'],
      currPhoto: json['curr_photo'],
      waterThreshold: json['water_threshold'],
      lightThreshold: json['light_threshold'],
    );
  }
}
// end PlantRequest

// updatePlant - makes request to http://localhost:5000/plants/all/update
Future<UpdateList> updatePlant(
    String id,
    String userEmail,
    String plantName,
    String species,
    String serialPort,
    String position,
    String currPhoto,
    String waterThreshold,
    String lightThreshold) async {
  final http.Response response = await http.put(
    // 'http://localhost:5000/plants/update/${id}',
    'http://backend-dev222222.us-east-1.elasticbeanstalk.com/plants/update/${id}',
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      "user_email": userEmail,
      "plant_name": plantName,
      "species": species,
      "serial_port": serialPort,
      "position": position,
      "curr_photo": currPhoto,
      "water_threshold": waterThreshold,
      "light_threshold": lightThreshold,
    }),
  );
  if (response.statusCode == 200) {
    return UpdateList.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load plant request');
  }
}
// end updatePlant

class _UpdatePlantPageState extends State<UpdatePlantPage> {
  // Future<Plant> futurePlant;
  // confirmUpdate;
  String plantName;
  String species;
  String userEmail;
  String uri;
  String serialPort;
  int position;
  int currPhoto;
  int waterThreshold;
  int lightThreshold;

  @override
  void initState() {
    super.initState();
    // futurePlant = fetchPlantInfo(widget.plantId);
    plantName = widget.plantName;
    species = widget.species;
    userEmail = widget.userEmail;
    uri = widget.uri;
    serialPort = widget.serialPort;
    position = widget.position;
    currPhoto = widget.currPhoto;
    waterThreshold = widget.waterThreshold;
    lightThreshold = widget.lightThreshold;
  }

  void updateValue(name, value) {
    if (name == 'plantName') {
      plantName = value;
    } else if (name == 'species') {
      species = value;
    } else if (name == 'userEmail') {
      userEmail = value;
    } else if (name == 'serialPort') {
      serialPort = value;
    } else if (name == 'position') {
      position = value;
    } else if (name == 'currPhoto') {
      currPhoto = value;
    } else if (name == 'waterThreshold') {
      waterThreshold = value;
    } else if (name == 'lightThreshold') {
      lightThreshold = value;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Stack(children: <Widget>[
      Container(
        decoration: BoxDecoration(
            image: DecorationImage(
                image: AssetImage("assets/bgimg_dashboard.jpg"),
                fit: BoxFit.cover)),
        child: Scaffold(
            backgroundColor: Colors.transparent,
            appBar: AppBar(
              elevation: 0,
              backgroundColor: Colors.transparent,
            ),
            body: SingleChildScrollView(
                // child: Center(
                child: Align(
                    // alignment: Alignment.centerLeft,
                    child: Column(children: <Widget>[
              Image.network(
                uri,
                height: 200.0,
                width: 200,
                fit: BoxFit.fill,
              ),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(Icons.person, plantName, "Name", "plantName",
                      updateValue)),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(FontAwesomeIcons.seedling, species, "Species",
                      "species", updateValue)),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(Icons.email, userEmail, "Email", "userEmail",
                      updateValue)),
              SizedBox(height: 20),
              Container(
                  width: 340.0,
                  child: EditForm(Icons.enhanced_encryption, serialPort,
                      "Serial port", "serialPort", updateValue)),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(Icons.crop_square, position.toString(),
                    "Position", "position", updateValue),
              ),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(FontAwesomeIcons.water, waterThreshold.toString(),
                    "Water threshold", "waterThreshold", updateValue),
              ),
              SizedBox(height: 20),
              Container(
                width: 340.0,
                child: EditForm(FontAwesomeIcons.lightbulb, lightThreshold.toString(),
                    "Light threshold", "lightThreshold", updateValue),
              ),
              SizedBox(height: 60),
              WideButtonGreen("Confirm", () {
                updatePlant(
                    widget.plantId.toString(),
                    userEmail,
                    plantName,
                    species,
                    serialPort,
                    position.toString(),
                    currPhoto.toString(),
                    waterThreshold.toString(),
                    lightThreshold.toString());
                Navigator.pop(context);
              }),
              SizedBox(height: 40),
            ])))),
      )
    ]));
  }
}
