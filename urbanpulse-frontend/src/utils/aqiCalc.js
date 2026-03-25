export const calculateIndianAQI = (pm25) => {
  if (!pm25 || pm25 < 0) return 0;
  
  let Ih, Il, BPh, BPl;
  
  if (pm25 <= 30) {
    Ih = 50; Il = 0; BPh = 30; BPl = 0;
  } else if (pm25 <= 60) {
    Ih = 100; Il = 51; BPh = 60; BPl = 31;
  } else if (pm25 <= 90) {
    Ih = 200; Il = 101; BPh = 90; BPl = 61;
  } else if (pm25 <= 120) {
    Ih = 300; Il = 201; BPh = 120; BPl = 91;
  } else if (pm25 <= 250) {
    Ih = 400; Il = 301; BPh = 250; BPl = 121;
  } else {
    Ih = 500; Il = 401; BPh = 500; BPl = 251; // Cap above 250
  }

  const aqi = Math.round(((Ih - Il) / (BPh - BPl)) * (pm25 - BPl) + Il);
  return Math.min(aqi, 500);
};

export const getAqiCategory = (aqi) => {
  if (aqi > 400) return "Severe";
  if (aqi > 300) return "Very Poor";
  if (aqi > 200) return "Poor";
  if (aqi > 100) return "Moderate";
  if (aqi > 50) return "Satisfactory";
  return "Good";
};
