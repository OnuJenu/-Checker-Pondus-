import React, { useState } from 'react';
import { View, Text, Image, StyleSheet, StatusBar, Pressable } from 'react-native';
import { GestureHandlerRootView, PanGestureHandler, State } from 'react-native-gesture-handler';
import { BlurView } from 'expo-blur';
import * as Progress from 'react-native-progress';

// Import lokalnych obrazów
import image1 from '../assets/images/matiz.jpg';
import image2 from '../assets/images/bmw.jpg';

const HomeScreen = () => {

  const [image1Votes, setImage1Votes] = useState(10);
  const [image2Votes, setImage2Votes] = useState(20);
  const [voted, setVoted] = useState(false);

  // Funkcja obsługująca kliknięcia na obrazy
  const handleImageClick = (imageNumber) => {
    if (voted) return;
    if (imageNumber === 1) {
      setImage1Votes((prev) => prev + 1);
    } else if (imageNumber === 2) {
      setImage2Votes((prev) => prev + 1);
    }
    setVoted(true);
  };

  // Funkcja obsługująca gest swipe
  const handleSwipe = (event) => {
    if (event.nativeEvent.state === State.END && !voted) {
      const { translationY } = event.nativeEvent;
      if (translationY < -50) {
        setImage1Votes((prev) => prev + 1);
      } else if (translationY > 50) {
        setImage2Votes((prev) => prev + 1);
      }
      setVoted(true);
    }
  };

  const totalVotes = image1Votes + image2Votes;
  const image1Progress = totalVotes > 0 ? image1Votes / totalVotes : 0;
  const image2Progress = totalVotes > 0 ? image2Votes / totalVotes : 0;


  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <View style={styles.container}>
        {/* StatusBar */}
        <StatusBar barStyle="light-content" translucent backgroundColor="transparent" />

        <PanGestureHandler onHandlerStateChange={handleSwipe}>
          <View style={{ flex: 1 }}>
            {/* Górne zdjęcie */}
            <View style={styles.imageContainer}>
              <Image source={image1} style={styles.image} resizeMode="cover" />
              {voted && (
                <>
                  <BlurView intensity={50} style={StyleSheet.absoluteFill} />
                  <View style={styles.overlay} />
                  <View style={styles.progressContainer}>
                    <Text style={styles.progressText}>{Math.round(image1Progress * 100)}%</Text>
                    <Progress.Bar
                      progress={image1Progress}
                      width={300}
                      color="#FFFFFF"
                      borderColor="#FFFFFF"
                      borderWidth={1}
                      height={8}
                      style={styles.progressBar}
                      animated={true} // Włączenie animacji
                      animationConfig={{ duration: 1000 }} // Konfiguracja animacji
                    />
                  </View>
                </>
              )}
              <Pressable onPress={() => handleImageClick(1)} style={StyleSheet.absoluteFill} />
            </View>

            {/* Pytanie */}
            <Text style={styles.question}>Którego zwierzaka mam wybrać?</Text>

            {/* Dolne zdjęcie */}
            <View style={styles.imageContainer}>
              <Image source={image2} style={styles.image} resizeMode="cover" />
              {voted && (
                <>
                  <BlurView intensity={50} style={StyleSheet.absoluteFill} />
                  <View style={styles.overlay} />
                  <View style={styles.progressContainer}>
                    <Text style={styles.progressText}>{Math.round(image2Progress * 100)}%</Text>
                    <Progress.Bar
                      progress={image2Progress}
                      width={300}
                      color="#FFFFFF"
                      borderColor="#FFFFFF"
                      borderWidth={1}
                      height={8}
                      style={styles.progressBar}
                      animated={true} // Włączenie animacji
                      animationConfig={{ duration: 500, useNativeDriver: false }} // Konfiguracja animacji
                    />
                  </View>
                </>
              )}
              <Pressable onPress={() => handleImageClick(2)} style={StyleSheet.absoluteFill} />
            </View>
          </View>
        </PanGestureHandler>
      </View>
    </GestureHandlerRootView>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  imageContainer: {
    position: 'relative',
    flex: 1,
    width: '100%',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  progressBar: {
    borderRadius: 50,
  },
  progressContainer: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  progressText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  question: {
    backgroundColor: '#15616D',
    color: '#FFFFFF',
    paddingVertical: 10,
    paddingHorizontal: 20,
    textAlign: 'center',
    fontSize: 18,
    fontWeight: 'bold',
    width: '100%',
  },
});

export default HomeScreen;
