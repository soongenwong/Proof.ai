import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Mic, FileText, Folder } from "lucide-react"

export default function Component() {
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
                <Button className="bg-black hover:bg-gray-800 text-white px-6 py-3 rounded-full mb-8">
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
                placeholder="Generated text from your call will appear here for editing..."
                className="min-h-32 resize-none border-gray-300"
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">0 words</span>
                <div className="space-x-3">
                  <Button variant="outline" className="text-gray-600 bg-transparent">
                    Clear
                  </Button>
                  <Button className="bg-black hover:bg-gray-800 text-white">Save Changes</Button>
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
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-gray-700">Brand Guidelines</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-gray-700">Due Diligence</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span className="text-gray-700">Market Research</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-gray-700">Business Model</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="text-gray-700">Financial Planning</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-teal-500 rounded-full"></div>
                <span className="text-gray-700">Legal Structure</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
