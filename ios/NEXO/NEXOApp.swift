import SwiftUI
import WebKit

@main
struct NEXOApp: App {
    var body: some Scene {
        WindowGroup {
            NEXORootView()
                .preferredColorScheme(.light)
        }
    }
}

struct NEXORootView: View {
    var body: some View {
        NEXOWebView()
            .ignoresSafeArea(edges: [])
            .background(Color(red: 0.957, green: 0.969, blue: 0.957))
    }
}

struct NEXOWebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 0.957, green: 0.969, blue: 0.957, alpha: 1)
        webView.scrollView.backgroundColor = webView.backgroundColor
        webView.allowsBackForwardNavigationGestures = false
        webView.scrollView.contentInsetAdjustmentBehavior = .automatic

        if let indexURL = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "WebAssets") {
            webView.loadFileURL(indexURL, allowingReadAccessTo: indexURL.deletingLastPathComponent())
        } else {
            let html = """
            <!doctype html><html lang="es"><meta name="viewport" content="width=device-width,initial-scale=1">
            <body style="font-family:-apple-system;padding:32px;color:#1d2b22"><h1>NEXO</h1>
            <p>No se encontraron los archivos de la aplicación. Vuelve a compilar desde GitHub.</p></body></html>
            """
            webView.loadHTMLString(html, baseURL: nil)
        }
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
