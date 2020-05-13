import 'package:flutter/material.dart';
import 'package:lets_head_out/Screens/DashBoard.dart';
import 'package:lets_head_out/Screens/OverViewScreen.dart';
import 'package:lets_head_out/Screens/UpdatePlantPage.dart';

import 'Screens/SplashScreen.dart';


void main() =>
    runApp(MaterialApp(home: SplashScreen(), title: 'Synthesis - The Automatic Garden',),
    // runApp(MaterialApp(home: SplashScreen(), title: 'Synthesis - The Automatic Garden', routes: <String, WidgetBuilder> {
    // 'Dashboard': (BuildContext context) => new Dashboard(),
    // 'OverView' : (BuildContext context) => new OverViewPage(),
    // 'UpdatePlant' : (BuildContext context) => new UpdatePlantPage(),
    // 'AddPlant' : (BuildContext context) => new Screen4(),
    // }),
    );
