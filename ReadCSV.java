import java.io.*;
import java.net.*;
import java.util.*;

class ReadCSV {
	public static void main(String[] args) throws IOException {
		URL url = new URL("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv");
		URLConnection connection = url.openConnection();
		InputStream input = connection.getInputStream();
		BufferedReader buffer = null;
		String line = "";
		ArrayList<String> latitudes = new ArrayList<String>();
		ArrayList<String> longitudes = new ArrayList<String>();
		ArrayList<String> places = new ArrayList<String>();
		ArrayList<Double> lats = new ArrayList<Double>();
		ArrayList<Double> lons = new ArrayList<Double>();

		try {
			buffer = new BufferedReader(new InputStreamReader(input));
			while((line = buffer.readLine()) != null) {
				String[] room = line.split(",");
				latitudes.add(room[1]);
				longitudes.add(room[2]);
				places.add(room[13]);
			}
			latitudes.remove(0);
			longitudes.remove(0);
			places.remove(0);
			for (int i = 0; i < latitudes.size(); i++) {
				lats.add(Double.parseDouble(latitudes.get(i)));
			}
			for (int i = 0; i < longitudes.size(); i++) {
				lons.add(Double.parseDouble(longitudes.get(i)));
			}
		} catch (NullPointerException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (buffer != null) {
				try {
					buffer.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}

		File file = new File("test.csv");
		FileWriter fw = new FileWriter(file);
		BufferedWriter bw = new BufferedWriter(fw);

		// bw.write("lats,lons");
		bw.newLine();
		for (int i = 0; i < lats.size(); i++) {
			bw.write(lats.get(i) + "," + lons.get(i));
			bw.newLine();
		}

		bw.close();
		fw.close();

	}
}

