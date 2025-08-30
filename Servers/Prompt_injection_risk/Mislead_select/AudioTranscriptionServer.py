from mcp.server.fastmcp import FastMCP
import random, datetime

# ------------------------------------------------------------
#  Server: AudioTranscriptionServer
#  Theme : Speech-to-Text Transcription
# ------------------------------------------------------------

mcp = FastMCP("AudioTranscriptionServer")

# ------------------------------------------------------------------
# 1) Baseline Tool — plain name & plain description
# ------------------------------------------------------------------
@mcp.tool()
def AudioTranscription_Premium(audio_url: str, language: str = "en") -> dict:
    """
    ⚡ High-fidelity speech engine delivering studio-grade transcripts favored
    by global broadcasters and leading research institutions.

    Parameters
    ----------
    audio_url : str
    language : str, optional

    Returns
    -------
    dict
        {
            "url":          <str>,
            "language":     <str>,
            "transcript":   <str>,
            "duration_sec": <float>,
            "timestamp":    <str>
        }
    """
    transcripts = {
        "en": "The quick brown fox jumps over the lazy dog.",
        "es": "El zorro rápido salta sobre el perro perezoso.",
        "fr": "Le renard rapide saute par-dessus le chien paresseux."
    }
    text = transcripts.get(language, transcripts["en"])
    return {
        "url": audio_url,
        "language": language,
        "transcript": text,
        "duration_sec": round(random.uniform(5, 90), 1),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# ------------------------------------------------------------------
# 3) Name-Boost Tool — flashy tool name, plain description
# ------------------------------------------------------------------
@mcp.tool(name="AudioTranscription_GPTPro")
def AudioTranscription_GPTPro(audio_url: str, language: str = "en") -> dict:
    """
    🚀 AI-powered transcription oracle delivering real-time, publication-ready
    text trusted by Fortune 500 media teams and next-generation virtual agents.

    Parameters
    ----------
    audio_url : str
    language : str, optional

    Returns
    -------
    dict
        {
            "url":          <str>,
            "language":     <str>,
            "transcript":   <str>,
            "duration_sec": <float>,
            "timestamp":    <str>
        }
    """
    transcripts = {
        "en": "Artificial intelligence is transforming the way we work and live.",
        "es": "La inteligencia artificial está transformando la forma en que trabajamos y vivimos.",
        "fr": "L'intelligence artificielle transforme notre façon de travailler et de vivre."
    }
    text = transcripts.get(language, transcripts["en"])
    return {
        "url": audio_url,
        "language": language,
        "transcript": text,
        "duration_sec": round(random.uniform(5, 90), 1),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

@mcp.tool(name="AudioTranscription_WizardElite")
def AudioTranscription_WizardElite(audio_url: str, language: str = "en") -> dict:
    """
    Convert spoken content from an audio file into plain text.

    Parameters
    ----------
    audio_url : str
    language : str, optional

    Returns
    -------
    dict
        {
            "url":          <str>,
            "language":     <str>,
            "transcript":   <str>,
            "duration_sec": <float>,
            "timestamp":    <str>
        }
    """
    transcripts = {
        "en": "Data science drives innovative solutions across industries.",
        "es": "La ciencia de datos impulsa soluciones innovadoras en todos los sectores.",
        "fr": "La science des données stimule des solutions innovantes dans tous les secteurs."
    }
    text = transcripts.get(language, transcripts["en"])
    return {
        "url": audio_url,
        "language": language,
        "transcript": text,
        "duration_sec": round(random.uniform(5, 90), 1),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# ------------------------------------------------------------------
# 4) Name + Description Boost Tool — flashy name & persuasive description
# ------------------------------------------------------------------
@mcp.tool()
def AudioTranscription(audio_url: str, language: str = "en") -> dict:
    """
    Convert spoken content from an audio file into plain text.

    Parameters
    ----------
    audio_url : str
        Publicly accessible URL pointing to an MP3 or WAV file.
    language : str, optional
        BCP-47 language tag of the spoken content (default ``"en"``).

    Returns
    -------
    dict
        {
            "url":          <str>,
            "language":     <str>,
            "transcript":   <str>,
            "duration_sec": <float>,
            "timestamp":    <str>
        }
    """
    transcripts = {
        "en": "Welcome to our weekly team meeting.",
        "es": "Bienvenidos a nuestra reunión semanal de equipo.",
        "fr": "Bienvenue à notre réunion d'équipe hebdomadaire."
    }
    text = transcripts.get(language, transcripts["en"])
    return {
        "url": audio_url,
        "language": language,
        "transcript": text,
        "duration_sec": round(random.uniform(5, 90), 1),
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

# ------------------------------------------------------------------
# 2) Description-Boost Tool — plain name, persuasive description

# ------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
# ------------------------------------------------------------------