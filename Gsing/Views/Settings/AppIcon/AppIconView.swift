import SwiftUI
import NimbleViews

struct AppIconView: View {
    private struct Option: Identifiable {
        let id: String
        let title: String
        let subtitle: String
        let alternateName: String?
    }

    private let options = [
        Option(id: "primary", title: "Default", subtitle: "Gsing", alternateName: nil)
    ]

    @State private var selectedIcon = UIApplication.shared.alternateIconName
    @State private var changing = false
    @State private var errorMessage: String?

    var body: some View {
        NBList(.localized("App Icon")) {
            NBSection(.localized("Available Icons")) {
                ForEach(options) { option in
                    Button {
                        changeIcon(option)
                    } label: {
                        HStack(spacing: 12) {
                            if let image = UIImage(named: option.alternateName ?? "AppIcon")
                                ?? (option.alternateName == nil ? UIImage(named: Bundle.main.iconFileName ?? "") : nil) {
                                Image(uiImage: image)
                                    .appIconStyle(size: 60)
                            } else {
                                Image("App_Unknown")
                                    .appIconStyle(size: 60)
                            }

                            VStack(alignment: .leading, spacing: 2) {
                                Text(.localized(option.title))
                                    .font(.headline)
                                    .foregroundStyle(.primary)
                                Text(option.subtitle)
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            if selectedIcon == option.alternateName {
                                Image(systemName: "checkmark")
                                    .foregroundStyle(Color.accentColor)
                                    .font(.headline)
                            }
                        }
                        .contentShape(Rectangle())
                        .padding(.vertical, 4)
                    }
                    .buttonStyle(.plain)
                    .disabled(changing)
                }
            }
        }
        .onAppear {
            selectedIcon = UIApplication.shared.alternateIconName
        }
        .alert(.localized("Unable to change app icon"), isPresented: Binding(
            get: { errorMessage != nil },
            set: { if !$0 { errorMessage = nil } }
        )) {
            Button(.localized("OK"), role: .cancel) { errorMessage = nil }
        } message: {
            Text(errorMessage ?? "")
        }
    }

    private func changeIcon(_ option: Option) {
        guard !changing, selectedIcon != option.alternateName else { return }
        changing = true
        UIApplication.shared.setAlternateIconName(option.alternateName) { error in
            DispatchQueue.main.async {
                changing = false
                selectedIcon = UIApplication.shared.alternateIconName
                if let error = error {
                    errorMessage = error.localizedDescription
                }
            }
        }
    }
}
