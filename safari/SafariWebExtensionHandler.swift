import SafariServices

final class SafariWebExtensionHandler: NSObject, NSExtensionRequestHandling {
    func beginRequest(with context: NSExtensionContext) {
        // No native messaging or calendar-data bridge is needed.
        context.completeRequest(returningItems: [], completionHandler: nil)
    }
}
