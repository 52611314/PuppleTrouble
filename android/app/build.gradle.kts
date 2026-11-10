import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

val localSettings = Properties().apply {
    val file = rootProject.file("local.properties")
    if (file.exists()) file.inputStream().use { load(it) }
}
fun apiUrl(value: String): String {
    require(value.startsWith("http://") || value.startsWith("https://")) { "API_BASE_URL 必须是 HTTP(S) 地址" }
    return "\"" + value.trimEnd('/').plus('/').replace("\\", "\\\\").replace("\"", "\\\"") + "\""
}

android {
    namespace = "com.puppletrouble.app"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.puppletrouble.app"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }
    buildTypes {
        debug {
            buildConfigField("String", "API_BASE_URL", apiUrl(localSettings.getProperty("API_BASE_URL", "http://10.0.2.2:8000/api/v1/")))
        }
        release {
            val releaseUrl = providers.gradleProperty("RELEASE_API_BASE_URL").orNull
            if (gradle.startParameter.taskNames.any { it.contains("release", ignoreCase = true) }) {
                require(releaseUrl?.startsWith("https://") == true) { "发布需设置 -PRELEASE_API_BASE_URL=https://实际服务/api/v1/" }
            }
            buildConfigField("String", "API_BASE_URL", apiUrl(releaseUrl ?: "https://unconfigured.invalid/api/v1/"))
            isMinifyEnabled = false
        }
    }
    buildFeatures { compose = true; buildConfig = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

kotlin { compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17) } }

dependencies {
    implementation(libs.activity.compose)
    implementation(libs.compose.ui)
    implementation(libs.compose.foundation)
    implementation(libs.compose.material3)
    implementation(libs.coroutines.android)
    testImplementation(libs.junit)
}
