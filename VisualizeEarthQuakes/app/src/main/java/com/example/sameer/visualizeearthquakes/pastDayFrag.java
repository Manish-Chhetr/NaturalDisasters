package com.example.sameer.visualizeearthquakes;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.MapsInitializer;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

public class pastDayFrag extends Fragment implements OnMapReadyCallback {

    GoogleMap mGoogleMap;
    MapView mMapView;
    View mView;
    ArrayList<String> latitudes = new ArrayList<>();
    ArrayList<String> longitudes = new ArrayList<>();
    ArrayList<String> places = new ArrayList<>();
    ArrayList<Double> lats = new ArrayList<>();
    ArrayList<Double> lons = new ArrayList<>();
    ArrayList<String> magnitude = new ArrayList<>();
    ArrayList<Double> mags = new ArrayList<>();
    String urlData = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv";

    public pastDayFrag() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        mView = inflater.inflate(R.layout.fragment_past_day, container, false);
        return mView;
    }

    @Override
    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        mMapView = mView.findViewById(R.id.map2);
        if (mMapView != null) {
            mMapView.onCreate(null);
            mMapView.onResume();
            mMapView.getMapAsync(this);
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        MapsInitializer.initialize(getContext());
        mGoogleMap = googleMap;
        googleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        new previousDay().execute();
    }

    public class previousDay extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... strings) {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(urlData);
                conn = (HttpURLConnection) url.openConnection();
                InputStream input = conn.getInputStream();
                if (conn.getResponseCode() == 200) {
                    BufferedReader br = new BufferedReader(new InputStreamReader(input));
                    String line;
                    while ((line = br.readLine()) != null) {
                        String[] room = line.split(",");
                        latitudes.add(room[1]);
                        longitudes.add(room[2]);
                        places.add(room[13]);
                        magnitude.add(room[4]);
                    }
                    latitudes.remove(0);
                    longitudes.remove(0);
                    places.remove(0);
                    magnitude.remove(0);
                    for (int i = 0; i < latitudes.size(); i++) {
                        lats.add(Double.parseDouble(latitudes.get(i)));
                        lons.add(Double.parseDouble(longitudes.get(i)));
                        mags.add(Double.parseDouble(magnitude.get(i)));
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (conn != null) {
                    conn.disconnect();
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            int height = 20;
            int width = 20;
            BitmapDrawable bitmp = (BitmapDrawable) getResources().getDrawable(R.drawable.dot);
            Bitmap b = bitmp.getBitmap();
            Bitmap smallMarker = Bitmap.createScaledBitmap(b, width, height, false);
            for (int i = 0; i < lats.size(); i++) {
                mGoogleMap.addMarker(new MarkerOptions().position(new LatLng(lats.get(i), lons.get(i)))
                        .title(places.get(i))
                        .snippet("Magnitude : " + mags.get(i))
                        .icon(BitmapDescriptorFactory.fromBitmap(smallMarker)));
            }

            mGoogleMap.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(lats.get(0), lons.get(0))));
        }

        @Override
        protected void onPreExecute() {

        }

    }

}
