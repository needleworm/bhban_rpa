package com.webview.rpa

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import com.webview.rpa.R

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView) // 웹뷰 객체 가져오기
        webView.webViewClient = WebViewClient() // 웹뷰 클라이언트 생성
        webView.settings.javaScriptEnabled = true
        webView.loadUrl("https://needleworm.github.io/bhban_rpa") // 해당 url 로딩

        if (savedInstanceState != null) webView.restoreState(savedInstanceState)
        else webView.loadUrl("https://needleworm.github.io/bhban_rpa")

    }
    override fun onBackPressed() {
        if (webView.canGoBack()) webView.goBack()
        else super.onBackPressed()
    }
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        webView.saveState(outState)
    }

}