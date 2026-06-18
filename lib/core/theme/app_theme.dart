import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  AppTheme._();

  // Renk Paleti (Cyber / Developer Dark Mode)
  static const Color darkBackground = Color(0xFF0F0F10);
  static const Color darkCard = Color(0xFF1E1E1F);
  static const Color primaryCyan = Color(0xFF00B0FF); // Siber Mavi
  static const Color accentNeonGreen = Color(0xFF00E676); // Neon Yeşil
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFF9E9E9E);
  static const Color borderNeutral = Color(0xFF2C2C2E);

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: darkBackground,
      primaryColor: primaryCyan,
      cardColor: darkCard,
      
      // Renk Şeması (Color Scheme)
      colorScheme: const ColorScheme.dark(
        surface: darkCard,
        primary: primaryCyan,
        secondary: accentNeonGreen,
        onPrimary: Colors.black,
        onSecondary: Colors.black,
        onSurface: textPrimary,
      ),

      // Kart Teması (CardThemeData)
      cardTheme: CardThemeData(
        color: darkCard,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: borderNeutral, width: 1),
        ),
      ),

      // AppBar Teması
      appBarTheme: AppBarTheme(
        backgroundColor: darkBackground,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.jetBrainsMono(
          color: textPrimary,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
        iconTheme: const IconThemeData(color: textPrimary),
      ),

      // Metin Teması (Typography)
      textTheme: TextTheme(
        displayLarge: GoogleFonts.jetBrainsMono(
          color: textPrimary,
          fontSize: 32,
          fontWeight: FontWeight.bold,
        ),
        titleLarge: GoogleFonts.jetBrainsMono(
          color: textPrimary,
          fontSize: 18,
          fontWeight: FontWeight.w600,
        ),
        bodyLarge: GoogleFonts.inter(
          color: textPrimary,
          fontSize: 16,
          fontWeight: FontWeight.normal,
        ),
        bodyMedium: GoogleFonts.inter(
          color: textSecondary,
          fontSize: 14,
          fontWeight: FontWeight.normal,
        ),
        labelLarge: GoogleFonts.jetBrainsMono(
          color: primaryCyan,
          fontSize: 12,
          fontWeight: FontWeight.bold,
        ),
      ),

      // Divider Teması
      dividerTheme: const DividerThemeData(
        color: borderNeutral,
        thickness: 1,
      ),
    );
  }
}
