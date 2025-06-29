"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Mic, FileText, Folder } from "lucide-react"

export default function StartupIdeation() {
  const [transcript, setTranscript] = useState("")
  const [wordCount, setWordCount] = useState(0)

  const handleTranscriptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value
    setTranscript(text)
    setWordCount(
      text
        .trim()
        .split(/\s+/)
        .filter((word) => word.length > 0).length,
    )
  }

  const handleClear = () => {
    setTranscript("")
    setWordCount(0)
  }

  const handleSaveChanges = () => {
    // Implement save functionality
    console.log("Saving changes:", transcript)
  }

  const handleStartCall = () => {
    // Implement call functionality
    console.log("Starting call...")
  }

  const topics = [
    { name: "Brand Guidelines", color: "bg-blue-500" },
    { name: "Due Diligence", color: "bg-green-500" },
    { name: "Market Research", color: "bg-purple-500" },
    { name: "Business Model", color: "bg-orange-500" },
    { name: "Financial Planning", color: "bg-red-500" },
    { name: "Legal Structure", color: "bg-teal-500" },
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Unicorn Labs - Startup Ideation</h1>
      </div>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-8">
          {/* Proof AI Section */}
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Proof AI</h2>
            <p className="text-gray-600 text-lg mb-8">How can I help you today?</p>

            {/* Circular Gradient Element */}
            <div className="flex justify-center mb-8">
              <div className="relative w-80 h-80 rounded-full bg-gradient-to-br from-blue-200 via-blue-300 to-slate-500 flex items-center justify-center shadow-lg">
                <Button
                  onClick={handleStartCall}
                  className="bg-black hover:bg-gray-800 text-white px-6 py-3 rounded-full mb-8"
                >
                  <Mic className="w-4 h-4 mr-2" />
                  Start a call
                </Button>
                <div className="absolute bottom-20 bg-white p-3 rounded-lg shadow-md">
                  <FileText className="w-6 h-6 text-gray-600" />
                </div>
              </div>
            </div>
          </div>

          {/* Call Transcript Section */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Call Transcript</h3>
            <div className="space-y-4">
              <Textarea
                value={transcript}
                onChange={handleTranscriptChange}
                placeholder="Generated text from your call will appear here for editing..."
                className="min-h-32 resize-none border-gray-300"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">{wordCount} words</span>
                <div className="space-x-3">
                  <Button variant="outline" onClick={handleClear} className="text-gray-600 bg-transparent">
                    Clear
                  </Button>
                  <Button onClick={handleSaveChanges} className="bg-black hover:bg-gray-800 text-white">
                    Save Changes
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-8">
          {/* Generated Video Section */}
          <Card className="bg-slate-800 text-white">
            <CardContent className="p-8 text-center">
              <div className="mb-4">
                <div className="w-16 h-16 bg-gray-600 rounded-full flex items-center justify-center mx-auto">
                  <Folder className="w-8 h-8 text-gray-400" />
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-2">Generated Video</h3>
              <p className="text-gray-300">Video will appear here after your call</p>
            </CardContent>
          </Card>

          {/* Key Startup Creation Topics */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Key Startup Creation Topics</h3>
            <div className="space-y-4">
              {topics.map((topic, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-3 cursor-pointer hover:bg-gray-100 p-2 rounded-md transition-colors"
                >
                  <div className={`w-2 h-2 ${topic.color} rounded-full`}></div>
                  <span className="text-gray-700">{topic.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
