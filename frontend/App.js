import React from 'react';
import { Image, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// Import ikon
import homeIcon from './assets/icons/home.png';
import addIcon from './assets/icons/add.png';
import profileIcon from './assets/icons/profile.png';
import shareIcon from './assets/icons/share.png';
import searchIcon from './assets/icons/search.png';

// Ekrany aplikacji
import HomeScreen from './screens/HomeScreen';
import AddQuestionScreen from './screens/AddQuestionScreen';
import ProfileScreen from './screens/ProfileScreen';
import SearchScreen from './screens/SearchScreen';
import ShareScreen from './screens/ShareScrean';


// Konfiguracja dolnego menu
const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused }) => {
            let iconSource;

            if (route.name === 'Home') {
              iconSource = homeIcon;
            } else if (route.name === 'AddQuestion') {
              iconSource = addIcon;
            } else if (route.name === 'Profile') {
              iconSource = profileIcon;
            } else if (route.name === 'Search') {
              iconSource = searchIcon;
            } else if (route.name === 'Share') {
              iconSource = shareIcon;
            }

            return (
              <Image
                source={iconSource}
                style={{
                  width: 24,
                  height: 24,
                  tintColor: focused ? '#ffffff' : '#8E8E93',
                }}
              />
            );
          },
          tabBarActiveTintColor: '#FFFFFF', // Kolor aktywnej ikony
          tabBarInactiveTintColor: '#8E8E93', // Kolor nieaktywnej ikony
          tabBarStyle: {
            backgroundColor: '#000000', // Czarny kolor dolnej nawigacji
            borderTopWidth: 0, // Opcjonalnie usuń górną ramkę
          },
          headerShown: false, // Ukrycie nagłówka
        })}
      >
        <Tab.Screen name="Home" component={HomeScreen} options={{ title: '' }} />
        <Tab.Screen name="AddQuestion" component={AddQuestionScreen} options={{ title: '' }} />
        <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: '' }} />
        <Tab.Screen name="Share" component={ShareScreen} options={{ title: '' }} />
        <Tab.Screen name="Search" component={SearchScreen} options={{ title: '' }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f5f5f5',
  },
});