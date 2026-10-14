import SwiftUI

@main
struct CalendarSeasonsApp: App {
    var body: some Scene { WindowGroup { WelcomeView() } }
}

struct WelcomeView: View {
    @Environment(\.openURL) private var openURL
    private let seasons: [(String, String, Color)] = [
        ("Winter Vibes", "snowflake", Color(red: 0.87, green: 0.94, blue: 0.98)),
        ("Cozy Fall", "leaf.fill", Color(red: 0.96, green: 0.88, blue: 0.76)),
        ("Spring Bloom", "camera.macro", Color(red: 0.98, green: 0.88, blue: 0.93)),
        ("Summer Glow", "sun.max.fill", Color(red: 0.99, green: 0.94, blue: 0.72))
    ]
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                Image(systemName: "calendar.badge.clock").font(.system(size: 44)).foregroundStyle(Color(red: 0.38, green: 0.49, blue: 0.40))
                Text("Welcome to\nCalendar Seasons").font(.system(size: 36, weight: .bold, design: .rounded))
                Text("A little seasonal celebration, every time you open your calendar.").font(.title3).foregroundStyle(.secondary)
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
                    ForEach(seasons, id: \.0) { season in
                        VStack(alignment: .leading, spacing: 20) {
                            Image(systemName: season.1).font(.largeTitle)
                            Text(season.0).font(.system(.headline, design: .rounded))
                        }.frame(maxWidth: .infinity, minHeight: 112, alignment: .leading)
                         .padding(16).background(season.2, in: RoundedRectangle(cornerRadius: 24)).foregroundStyle(Color(red: 0.25, green: 0.32, blue: 0.29))
                    }
                }
                VStack(alignment: .leading, spacing: 20) {
                    Text("Your first little transformation").font(.title2.bold())
                    step("1", "Enable the extension", "Open Settings → Apps → Safari → Extensions → Calendar Seasons. Turn on Allow Extension. On older iOS versions, Safari is directly in Settings.")
                    step("2", "Allow Google Calendar", "Open calendar.google.com in Safari. Use the Page Menu (or aA on older iOS) → Manage Extensions to enable Calendar Seasons. Allow access for this website when Safari asks.")
                    step("3", "Pick your mood", "In Safari’s Page Menu, tap Calendar Seasons to open its settings. Choose a theme or follow the seasons automatically.")
                }.padding(22).background(.background, in: RoundedRectangle(cornerRadius: 26))
                Button { openURL(URL(string: "https://calendar.google.com/calendar/")!) } label: {
                    Label("Open Google Calendar", systemImage: "arrow.up.right").font(.headline).frame(maxWidth: .infinity).padding(18)
                }.buttonStyle(.borderedProminent).tint(Color(red: 0.38, green: 0.49, blue: 0.40)).clipShape(RoundedRectangle(cornerRadius: 18))
                Text("Opens in your default browser. If that is not Safari, open calendar.google.com in Safari manually.").font(.footnote).foregroundStyle(.secondary)
                Text("Made for the Safari website").font(.headline)
                Text("Calendar Seasons styles the Google Calendar website in Safari, not the native Google Calendar app. Mobile website layouts may show fewer decorations. Your events stay untouched. Preferences stay on this device.").font(.footnote).foregroundStyle(.secondary)
            }.padding(24)
        }.background(Color(red: 0.97, green: 0.97, blue: 0.94)).navigationTitle("Calendar Seasons")
    }
    private func step(_ number: String, _ title: String, _ description: String) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Text(number).font(.headline).frame(width: 30, height: 30).background(Color.green.opacity(0.12), in: Circle())
            VStack(alignment: .leading, spacing: 5) { Text(title).font(.headline); Text(description).font(.subheadline).foregroundStyle(.secondary) }
        }
    }
}
