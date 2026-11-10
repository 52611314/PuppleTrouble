package com.puppletrouble.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.puppletrouble.app.data.HealthRepository
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = lightColorScheme(primary = Color(0xFF7550A5))) {
                Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFFF8F6F2)) { StartupScreen() }
            }
        }
    }
}

@Composable
private fun StartupScreen() {
    val repository = remember { HealthRepository() }
    val scope = rememberCoroutineScope()
    var status by remember { mutableStateOf("正在检查后端连接…") }
    var detail by remember { mutableStateOf("") }
    var checking by remember { mutableStateOf(false) }
    suspend fun refresh() {
        checking = true
        try {
            detail = repository.check()
            status = "后端连接正常"
        } catch (cancelled: CancellationException) { throw cancelled
        } catch (_: Exception) {
            status = "后端尚未连接"
            detail = "请启动后端并核对模拟器或真机的 API 地址。"
        } finally { checking = false }
    }
    LaunchedEffect(Unit) { refresh() }
    Column(Modifier.fillMaxSize().systemBarsPadding().padding(28.dp), verticalArrangement = Arrangement.spacedBy(24.dp)) {
        Text("玩犊紫", fontSize = 28.sp, color = Color(0xFF7550A5))
        Text("PuppleTrouble", color = Color(0xFF82758B))
        Text("让喜欢的颜色，\n成为你的表达。", fontSize = 30.sp, lineHeight = 44.sp)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf(0xFF7550A5, 0xFFC4ADD9, 0xFFF0C1A4, 0xFFF0E9DF, 0xFF394E4B).forEach {
                Box(Modifier.weight(1f).height(74.dp).background(Color(it), RoundedCornerShape(12.dp)))
            }
        }
        Text("本地示例配色 · 产品功能将在后续开发中加入", fontSize = 12.sp, color = Color(0xFF82758B))
        Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFF0EBF5))) {
            Column(Modifier.padding(22.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                Text(status, fontSize = 20.sp)
                Text(detail, fontSize = 13.sp)
                Text(BuildConfig.API_BASE_URL, fontSize = 11.sp)
                Button(enabled = !checking, onClick = { scope.launch { refresh() } }) { Text(if (checking) "检查中…" else "重新检查连接") }
            }
        }
        Text("工程初始化版本 · 0.1.0", fontSize = 12.sp, color = Color(0xFF82758B))
    }
}
