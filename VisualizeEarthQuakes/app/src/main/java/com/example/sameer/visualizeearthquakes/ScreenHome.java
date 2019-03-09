package com.example.sameer.visualizeearthquakes;

import android.support.annotation.NonNull;
import android.support.design.widget.NavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MenuItem;

public class ScreenHome extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener{

    private DrawerLayout mDrawer;
    private ActionBarDrawerToggle mToggle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_screen_home);
        mDrawer = findViewById(R.id.draw);
        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        mToggle = new ActionBarDrawerToggle(this, mDrawer, R.string.open, R.string.close);
        mDrawer.addDrawerListener(mToggle);
        mToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (mToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
        switch (menuItem.getItemId()) {
            case R.id.home:
                Fragment fh = new doChange();
                FragmentTransaction fth = getSupportFragmentManager().beginTransaction();
                fth.replace(R.id.place_y, fh).commit();
                break;
            case R.id.p_hour:
                Fragment fph = new pastHourFrag();
                FragmentTransaction ftph = getSupportFragmentManager().beginTransaction();
                ftph.replace(R.id.place_y, fph).commit();
                break;
            case R.id.p_day:
                Fragment fpd = new pastDayFrag();
                FragmentTransaction ftpd = getSupportFragmentManager().beginTransaction();
                ftpd.replace(R.id.place_y, fpd).commit();
                break;
            case R.id.p_week:
                Fragment fpw = new pastWeekFrag();
                FragmentTransaction ftpw = getSupportFragmentManager().beginTransaction();
                ftpw.replace(R.id.place_y, fpw).commit();
                break;
            case R.id.p_month:

                break;
            case R.id.logout:
                finish();
        }
        mDrawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
