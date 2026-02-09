package com.example.mementoandroid.data

import android.util.Log
import io.github.jan.supabase.createSupabaseClient
import io.github.jan.supabase.auth.Auth
import io.github.jan.supabase.auth.providers.builtin.Email
import io.github.jan.supabase.auth.auth

object Supabase {

    // 1. Initialize the Client
    // Replace these with your actual values from the Supabase Dashboard
    private const val SUPABASE_URL = "https://mtxdocmgvrvbiuicqikk.supabase.co"
    private const val SUPABASE_KEY = "sb_publishable_huKNKKeTyexTYF9a-cpYUQ_0iW4Yy7H"

    val client = createSupabaseClient(
        supabaseUrl = SUPABASE_URL,
        supabaseKey = SUPABASE_KEY
    ) {
        install(Auth)
    }

    // 2. Sign Up Function
    suspend fun signUp(emailInput: String, passwordInput: String): Result<String> {
        return try {
            client.auth.signUpWith(Email) {
                email = emailInput
                password = passwordInput
            }
            Result.success("Sign up successful! Please check your email for verification.")
        } catch (e: Exception) {
            Log.e("SupabaseAuth", "Sign up failed", e)
            Result.failure(e)
        }
    }

    // 3. Sign In Function
    suspend fun signIn(emailInput: String, passwordInput: String): Result<String> {
        return try {
            client.auth.signInWith(Email) {
                email = emailInput
                password = passwordInput
            }
            Result.success("Sign in successful!")
        } catch (e: Exception) {
            Log.e("SupabaseAuth", "Sign in failed", e)
            Result.failure(e)
        }
    }

    // 4. Check if user is already logged in (Useful for auto-login)
    suspend fun isUserLoggedIn(): Boolean {
        // This ensures the session is valid and refreshes the token if needed
        return client.auth.currentSessionOrNull() != null
    }
}