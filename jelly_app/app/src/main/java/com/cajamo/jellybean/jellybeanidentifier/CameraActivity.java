/* Copyright 2017 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

package com.cajamo.jellybean.jellybeanidentifier;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

/**
 * Main {@code Activity} class for the Camera app.
 */
public class CameraActivity extends Activity {

    private boolean isFlash;
    private boolean isLive = true;

    public void swapModes(View view) {
        Camera2BasicFragment fragment = (Camera2BasicFragment) getFragmentManager().findFragmentById(R.id.container);
        fragment.toggleLive(isLive = !isLive);
        ImageButton btn = findViewById(R.id.video_button);

        if (isLive) {
            btn.setImageResource(R.drawable.ic_camera_alt_black_24dp);
        } else {
            btn.setImageResource(R.drawable.ic_videocam_black_24dp);
        }
    }

    public void turnLightOn(View view) {
        Camera2BasicFragment fragment = (Camera2BasicFragment) getFragmentManager().findFragmentById(R.id.container);
        fragment.toggleFlash(isFlash = !isFlash);
        ImageButton btn = findViewById(R.id.flash_button);
        if (isFlash) {
            btn.setImageResource(R.drawable.ic_flash_on_white_24dp);
        } else {
            btn.setImageResource(R.drawable.ic_flash_off_black_24dp);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        if (null == savedInstanceState) {
            getFragmentManager()
                    .beginTransaction()
                    .replace(R.id.container, Camera2BasicFragment.newInstance())
                    .commit();
        }
    }
}
