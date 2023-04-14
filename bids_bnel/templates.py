import pandas as pd

template_participants = {
    "participant_id": "anonymised participant IDs of dataset",
    "species": "species of the participant",
    "sex": {
        "Description": "sex of the participant",
        "Levels": {
            "M": "male",
            "F": "female"
        }
    },
}

template_sessions = {
    'session-id': "Session identification tag",
    "comments": "Miscellaneous comments on study, interview, methodology relevant to this form data"
}

template_ieeg = {
    "TaskName": "clinic",
    "InstitutionName": "Bioelectronics Neurophysiology and Engineering Lab",
    "InstitutionAddress": "200 First Street SW, Rochester, MN 55905",
    "Manufacturer": "",
    "ManufacturersModelName": "",
    "SoftwareVersions": "",
    "TaskDescription": "",
    "Instructions": "",
    "iEEGReference": "intracranial average",
    "SamplingFrequency": "",
    "PowerLineFrequency": "",
    "SoftwareFilters": "",
    "HardwareFilters": "",
    "ElectrodeManufacturer": "",
    "ECOGChannelCount": "",
    "SEEGChannelCount": "",
    "EEGChannelCount": "",
    "EOGChannelCount": "",
    "ECGChannelCount": "",
    "EMGChannelCount": "",
    "MiscChannelCount": "",
    "RecordingDuration": "",
    "RecordingType": "continuous",
    "iEEGGround": "Unknown",
    "iEEGPlacementScheme": "Unknown",
    "iEEGElectrodeGroups": "Unknown",
    "SubjectArtefactDescription": "None",
    "ElectricalStimulation": False
}

template_electrodes = {
	"name": "Name of the electrode",
	"x": "x position of the electrode on the brain of the subject",
	"y": "y position of the electrode on the brain of the subject",
	"z": "z position of the electrode on the brain of the subject",
	"size": "Surface size in mm2 of the electrode",
	"material": "Material of the electrode. This is platinum in most situations",
	"manufacturer": "Manufacturer of the electrode",
	"group": "Group to which electrode belongs, this can be grid, strip, depth or other",
	"hemisphere": "Hemisphere where electrodes are placed. This can be right\/left\/right and left",
	"soz": "",
	"resected": "",
}

template_coordsystem = {
	"iEEGCoordinateSystem": "",
	"iEEGCoordinateUnits": "",
	"iEEGCoordinateSystemDescription": "",
	"iEEGCoordinateProcessingDescription": "",
	"iEEGCoordinateProcessingReference": ""
}

template_channels = {
    "name": "Name of the channel",
    "type": "Type of channel",
    "units": "Physical unit of the data represented in this channel",
    "low_cutoff": "Frequency used for the low cut off in Hz",
    "high_cutoff": "Frequency used for the high cut off in Hz",
    "reference": "Reference channel",
}

template_events = {
    "onset": {
        "type": "object",
        "description": "onset of event in seconds"
    },
    "duration": {
        "type": "object",
        "description": "duration of event in seconds"
    },
    "trial_type": {
        "type": "object",
        "description": "type of event (electrical stimulation\/motor task\/sensing task\/artefact\/sleep\/sleep wake transition\/eyes open)"
    },
    "sub_type": {
        "type": "object",
        "description": "more description of event (sleep:nrem\/rem, motor:Mario\/hand\/jump, sens:circle, electrical stimulation:SPES\/ESM\/REC2stim, seizure:clinical\/subclinical)"
    },
    "electrodes_involved_onset": {
        "type": "object",
        "description": "electrodes involved in onset. For example: electrodes involved in seizure onset or in artefact."
    },
    "electrodes_involved_offset": {
        "type": "object",
        "description": "electrodes involved in offset. For example: electrodes involved in the end of a seizure or in an artefact."
    },
    "offset": {
        "type": "object",
        "description": "offset of event in seconds"
    },
    "sample_start": {
        "type": "object",
        "description": "onset of event in samples"
    },
    "sample_end": {
        "type": "object",
        "description": "offset of event in samples"
    },
    "electrical_stimulation_type": {
        "type": "object",
        "description": "type of electrical stimulation [mono-\/biphasic]"
    },
    "electrical_stimulation_site": {
        "type": "object",
        "description": "electrode names of stimulus pair"
    },
    "electrical_stimulation_current": {
        "type": "object",
        "description": "electrical stimulation current in Ampere"
    },
    "electrical_stimulation_frequency": {
        "type": "object",
        "description": "electrical stimulation frequency in Hertz"
    },
    "electrical_stimulation_pulsewidth": {
        "type": "object",
        "description": "electrical stimulation pulse width in s"
    },
    "notes": {
        "type": "object",
        "description": "notes about the specific event"
    }
}

templates = {
    "participants": template_participants,
    "sessions": template_sessions,
    "ieeg": template_ieeg,
    "electrodes": template_electrodes,
    "coordsystem": template_coordsystem,
    "channels": template_channels,
    "events": template_events
}
