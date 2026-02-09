package com.example.mementoandroid

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBox
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import com.example.mementoandroid.ui.theme.MementoAndroidTheme
import com.example.mementoandroid.data.Supabase
import com.example.mementoandroid.ui.auth.AuthScreen
import kotlinx.coroutines.launch
import io.github.jan.supabase.auth.auth
import androidx.compose.runtime.rememberCoroutineScope

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MementoAndroidTheme {
                MementoAppRoot()
            }
        }
    }
}

@Composable
fun MementoAppRoot() {
    // 1. Separate states to avoid "Boolean?" compiler issues
    var isLoading by rememberSaveable { mutableStateOf(true) }
    var isUserLoggedIn by rememberSaveable { mutableStateOf(false) }

    // 2. Check Supabase session on launch
    LaunchedEffect(Unit) {
        // Assume Supabase.isUserLoggedIn() returns a Boolean
        isUserLoggedIn = Supabase.isUserLoggedIn()
        isLoading = false
    }

    // 3. Simple If/Else logic
    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else if (isUserLoggedIn) {
        MementoAndroidApp(
            onLogout = {
                // Handle logout
                isUserLoggedIn = false
            }
        )
    } else {
        AuthScreen(
            onLoginSuccess = {
                isUserLoggedIn = true
            }
        )
    }
}

@PreviewScreenSizes
@Composable
fun MementoAndroidApp(onLogout: () -> Unit = {}) {
    var currentDestination by rememberSaveable { mutableStateOf(AppDestinations.HOME) }

    NavigationSuiteScaffold(
        navigationSuiteItems = {
            AppDestinations.entries.forEach {
                item(
                    icon = {
                        Icon(
                            it.icon,
                            contentDescription = it.label
                        )
                    },
                    label = { Text(it.label) },
                    selected = it == currentDestination,
                    onClick = { currentDestination = it }
                )
            }
        }
    ) {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
            when(currentDestination) {
                AppDestinations.HOME -> Greeting(name = "Home", modifier = Modifier.padding(innerPadding))
                AppDestinations.FAVORITES -> Greeting(name = "Favorites", modifier = Modifier.padding(innerPadding))
                AppDestinations.PROFILE -> {
                    // Example of passing the logout function to the Profile screen
                    ProfileScreen(modifier = Modifier.padding(innerPadding), onLogout = onLogout)
                }
            }
        }
    }
}

@Composable
fun ProfileScreen(modifier: Modifier = Modifier, onLogout: () -> Unit) {
    // 1. Create a scope bound to this UI component
    val scope = rememberCoroutineScope()

    androidx.compose.foundation.layout.Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = androidx.compose.foundation.layout.Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("User Profile")
        androidx.compose.material3.Button(onClick = {
            // 2. Use that scope to launch the suspend function
            scope.launch {
                Supabase.client.auth.signOut()
                onLogout()
            }
        }) {
            Text("Log Out")
        }
    }
}

enum class AppDestinations(
    val label: String,
    val icon: ImageVector,
) {
    HOME("Home", Icons.Default.Home),
    FAVORITES("Favorites", Icons.Default.Favorite),
    PROFILE("Profile", Icons.Default.AccountBox),
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name- Memento!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MementoAndroidTheme {
        Greeting("Android")
    }
}