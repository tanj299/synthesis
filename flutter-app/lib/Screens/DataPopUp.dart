import 'package:flutter/material.dart';
import 'package:lets_head_out/utils/TextStyles.dart';

import 'dart:convert';
import 'package:http/http.dart' as http;

class DataPopUp extends StatefulWidget {
  final int plantId;
  DataPopUp({Key key, @required this.plantId}) : super(key: key);

  @override
  _DataPopUpState createState() => _DataPopUpState();
}

class PlantDataLogList {
  final List<PlantDataLog> plants;
  PlantDataLogList({
    this.plants,
  });
  factory PlantDataLogList.fromJson(List<dynamic> parsedJson) {
    List<PlantDataLog> plants = new List<PlantDataLog>();
    plants = parsedJson
        .map((plantJson) => PlantDataLog.fromJson(plantJson))
        .toList();
    return new PlantDataLogList(plants: plants);
  }
}

class PlantDataLog {
  final String plantId;
  final String humidity;
  final String light;
  final String lightStatus;
  final String soilMoisture;
  final String soilTemp;
  final String temp;
  final String timestamp;
  final String waterLevel;

  // constructor
  PlantDataLog({
    this.plantId,
    this.humidity,
    this.light,
    this.lightStatus,
    this.soilMoisture,
    this.soilTemp,
    this.temp,
    this.timestamp,
    this.waterLevel,
  });

  factory PlantDataLog.fromJson(Map<String, dynamic> json) {
    return PlantDataLog(
      plantId: json['plant_id'].toString(),
      humidity: json['humidity'],
      light: json['light'],
      lightStatus: json['light_status'],
      soilMoisture: json['soil_moisture'],
      soilTemp: json['soil_temp'],
      temp: json['temp'],
      timestamp: json['timestamp'],
      waterLevel: json['water_level'],
    );
  }
}

Future<PlantDataLogList> fetchPlantDataInfo(id) async {
  final response = await http.get(
      'http://localhost:5000/logs/all/${id}');
  // final response = await http.get(
  //     'http://backend-dev222222.us-east-1.elasticbeanstalk.com/logs/all/${id}');

  if (response.statusCode == 200) {
    return PlantDataLogList.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load plant');
  }
}

class _DataPopUpState extends State<DataPopUp> {
  Future<PlantDataLogList> futurePlantDataLogList;
  @override
  void initState() {
    super.initState();
    futurePlantDataLogList = fetchPlantDataInfo(widget.plantId);
  }

  Widget build(BuildContext context) {
    return new AlertDialog(
      title: const Text('Latest plant data logs'),
      content: new Container(
          height: 300,
          width: 300,
          child: FutureBuilder<PlantDataLogList>(
            future: futurePlantDataLogList,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                int numPlants = snapshot
                    .data.plants.length; // returns length of plants array
                List<Widget> plantsRender = new List<Widget>();
                for (var j = 0; j < numPlants; j++) {
                  int i = numPlants - j - 1; // do in descending order to get most recent first
                  plantsRender.add(BoldText(
                      (j + 1).toString() + ") " + snapshot.data.plants[i].timestamp + " - " + snapshot.data.plants[i].humidity,
                      15.0,
                      Colors.black));
                  plantsRender.add(SizedBox(
                    height: 5.0,
                  ));
                }
                return Container(
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
          )),
      actions: <Widget>[
        new FlatButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          textColor: Theme.of(context).primaryColor,
          child: const Text('Back'),
        ),
      ],
    );
  }
}
