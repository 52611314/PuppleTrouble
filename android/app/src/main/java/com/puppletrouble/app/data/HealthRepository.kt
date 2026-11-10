package com.puppletrouble.app.data

import com.puppletrouble.app.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class HealthRepository {
    suspend fun check(): String = withContext(Dispatchers.IO) {
        val connection = URL(BuildConfig.API_BASE_URL + "health").openConnection() as HttpURLConnection
        try {
            connection.connectTimeout = 5000
            connection.readTimeout = 5000
            check(connection.responseCode == 200) { "服务暂时不可用" }
            val result = connection.inputStream.bufferedReader().use { JSONObject(it.readText()) }.getJSONObject("data")
            check(result.getString("status") == "ok")
            "${result.getString("service")} · v${result.getString("version")}"
        } finally { connection.disconnect() }
    }
}
