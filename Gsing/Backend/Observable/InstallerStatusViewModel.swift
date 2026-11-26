//
//  StatusViewModel.swift
//  Feather
//
//  Created by samara on 24.04.2025.
//

import Foundation
import Combine
import IDeviceSwift

extension InstallerStatusViewModel {
	
	var statusImage: String {
		switch status {
		case .none: return "archivebox.fill"
		case .ready: return "app.gift"
		case .sendingManifest, .sendingPayload: return "paperplane.fill"
		case .installing: return "square.and.arrow.down"
		case .completed: return "app.badge.checkmark"
		case .broken: return "exclamationmark.triangle.fill"
		}
	}
	
	var statusLabel: String {
		switch status {
		case .none: return NSLocalizedString("Packaging", comment: "")
		case .ready: return NSLocalizedString("Ready", comment: "")
		case .sendingManifest: return NSLocalizedString("Sending Manifest", comment: "")
		case .sendingPayload: return NSLocalizedString("Sending Payload", comment: "")
		case .installing: return NSLocalizedString("Installing", comment: "")
		case .completed: return NSLocalizedString("Completed", comment: "")
		case .broken: return NSLocalizedString("Error", comment: "")
		}
	}
}
