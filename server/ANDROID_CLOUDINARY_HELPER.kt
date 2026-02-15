/**
 * Cloudinary Upload Helper for Android
 * 
 * Simple one-function upload: Just pass the image file and get the URL back!
 * 
 * Usage:
 *   val imageUrl = CloudinaryHelper.uploadImage(context, imageFile, authToken)
 * 
 * Setup:
 *   1. Add dependencies to build.gradle
 *   2. Set BASE_URL in this file
 *   3. Call uploadImage() with your image file
 */

package com.example.mementoandroid.utils

import android.content.Context
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject
import java.io.File
import java.io.IOException

object CloudinaryHelper {
    
    // TODO: Set your backend base URL
    private const val BASE_URL = "http://your-server:8000"
    
    private val client = OkHttpClient()
    
    /**
     * Upload an image to Cloudinary and return the URL.
     * 
     * @param context Android context
     * @param imageFile The image file to upload
     * @param authToken Your JWT authentication token (from login)
     * @return The Cloudinary URL of the uploaded image, or null if upload failed
     */
    suspend fun uploadImage(
        context: Context,
        imageFile: File,
        authToken: String
    ): String? = withContext(Dispatchers.IO) {
        try {
            // Step 1: Get upload signature from backend
            val signature = getUploadSignature(authToken, isImage = true)
                ?: return@withContext null
            
            // Step 2: Upload directly to Cloudinary
            val imageUrl = uploadToCloudinary(imageFile, signature, isImage = true)
            
            Log.d("CloudinaryHelper", "Image uploaded successfully: $imageUrl")
            imageUrl
            
        } catch (e: Exception) {
            Log.e("CloudinaryHelper", "Upload failed: ${e.message}", e)
            null
        }
    }
    
    /**
     * Upload an audio file to Cloudinary and return the URL.
     * 
     * @param context Android context
     * @param audioFile The audio file to upload
     * @param authToken Your JWT authentication token (from login)
     * @return The Cloudinary URL of the uploaded audio, or null if upload failed
     */
    suspend fun uploadAudio(
        context: Context,
        audioFile: File,
        authToken: String
    ): String? = withContext(Dispatchers.IO) {
        try {
            // Step 1: Get upload signature from backend
            val signature = getUploadSignature(authToken, isImage = false)
                ?: return@withContext null
            
            // Step 2: Upload directly to Cloudinary
            val audioUrl = uploadToCloudinary(audioFile, signature, isImage = false)
            
            Log.d("CloudinaryHelper", "Audio uploaded successfully: $audioUrl")
            audioUrl
            
        } catch (e: Exception) {
            Log.e("CloudinaryHelper", "Upload failed: ${e.message}", e)
            null
        }
    }
    
    /**
     * Get upload signature from backend
     */
    private suspend fun getUploadSignature(
        authToken: String,
        isImage: Boolean
    ): UploadSignature? = withContext(Dispatchers.IO) {
        try {
            val endpoint = if (isImage) {
                "$BASE_URL/upload/signature/image"
            } else {
                "$BASE_URL/upload/signature/audio"
            }
            
            val request = Request.Builder()
                .url(endpoint)
                .addHeader("Authorization", "Bearer $authToken")
                .get()
                .build()
            
            val response = client.newCall(request).execute()
            
            if (!response.isSuccessful) {
                Log.e("CloudinaryHelper", "Failed to get signature: ${response.code}")
                return@withContext null
            }
            
            val json = JSONObject(response.body?.string() ?: "")
            UploadSignature(
                uploadUrl = json.getString("upload_url"),
                cloudName = json.getString("cloud_name"),
                apiKey = json.getString("api_key"),
                timestamp = json.getInt("timestamp"),
                signature = json.getString("signature"),
                folder = json.getString("folder")
            )
        } catch (e: Exception) {
            Log.e("CloudinaryHelper", "Error getting signature: ${e.message}", e)
            null
        }
    }
    
    /**
     * Upload file directly to Cloudinary
     */
    private suspend fun uploadToCloudinary(
        file: File,
        signature: UploadSignature,
        isImage: Boolean
    ): String? = withContext(Dispatchers.IO) {
        try {
            val mediaType = if (isImage) {
                "image/*".toMediaType()
            } else {
                "audio/*".toMediaType()
            }
            
            val requestBody = MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", file.name, file.asRequestBody(mediaType))
                .addFormDataPart("api_key", signature.apiKey)
                .addFormDataPart("timestamp", signature.timestamp.toString())
                .addFormDataPart("signature", signature.signature)
                .addFormDataPart("folder", signature.folder)
                .apply {
                    if (!isImage) {
                        // Audio files need resource_type = "raw"
                        addFormDataPart("resource_type", "raw")
                    }
                }
                .build()
            
            val request = Request.Builder()
                .url(signature.uploadUrl)
                .post(requestBody)
                .build()
            
            val response = client.newCall(request).execute()
            
            if (!response.isSuccessful) {
                Log.e("CloudinaryHelper", "Cloudinary upload failed: ${response.code} - ${response.message}")
                return@withContext null
            }
            
            val json = JSONObject(response.body?.string() ?: "")
            json.getString("secure_url") // Return the image/audio URL
            
        } catch (e: Exception) {
            Log.e("CloudinaryHelper", "Error uploading to Cloudinary: ${e.message}", e)
            null
        }
    }
    
    /**
     * Data class for upload signature
     */
    private data class UploadSignature(
        val uploadUrl: String,
        val cloudName: String,
        val apiKey: String,
        val timestamp: Int,
        val signature: String,
        val folder: String
    )
}
