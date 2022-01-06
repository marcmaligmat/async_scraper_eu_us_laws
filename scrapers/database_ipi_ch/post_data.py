def post_data_from_latest(items_size, cursor):
    """Cursor is needed to get the next results"""

    return {
        "~#resultmeta": {
            "~:page-items": items_size,
            "~:total-items": 941482,
            "~:max-score": {"~#opt": 1.0},
            "~:cursor": {"~#opt": cursor},
            "~:processing-time": {"~#millis": 206},
            "~:query": {
                "~#query": {
                    "~:target": {"~#queryTarget": "chmarke"},
                    "~:page-size": items_size,
                    "~:extra-params": {
                        "~#lmm": {
                            "qf": [
                                "titel__type_text^6.0 wortbestandteil__type_text^5.0 markennummer__type_int^4.0 markennummer_formatiert__type_string^4.0 gesuchsnummer__type_text_split_num^3.0 ra_inhaber__type_text_mv^2.0 ra_vertreter__type_text_mv^1.0 wdltext__type_text^1.0 wdlklassennummer__type_text_mv^1.0 markennummer__type_text_split_num^4.0"
                            ]
                        }
                    },
                    "~:select": [
                        {"~#field": "datastore_checksum__type_string"},
                        {"~#field": "verfahrenssprache__type_string"},
                        {
                            "~#field": {
                                "~:name": "ra_unterlizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "markennummer_formatiert__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "_version_",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SYNTHETIC"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "loeschgrund__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_nutzniesser__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "erneuertemarke__type_boolean"},
                        {
                            "~#field": "quelleersteveroeffentlichung_publikationsziel__type_i18n"
                        },
                        {
                            "~#field": {
                                "~:name": "verkehrsdurchsetzung__type_boolean",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "schutztitelstadium__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "verfahrenssprache__type_i18n"},
                        {"~#field": "wdl__type_text_mv"},
                        {
                            "~#field": {
                                "~:name": "loeschdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "publikationsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": "quelleersteveroeffentlichung_ausgabe__type_string"
                        },
                        {
                            "~#field": {
                                "~:name": "officeorigincode__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "verkehrsdurchsetzung__type_i18n"},
                        {
                            "~#field": {
                                "~:name": "hinterlegungsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "farbanspruch__type_text"},
                        {
                            "~#field": {
                                "~:name": "doctype",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_pfandnehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ipikontoid__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "eintragungsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_vertreter__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_screen_hash__type_string_mv"},
                        {"~#field": "markennummer__type_int"},
                        {
                            "~#field": {
                                "~:name": "schutztiteltyp__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "spezialmarken__type_i18n_mv"},
                        {
                            "~#field": {
                                "~:name": "anmeldereferenz__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "markennummer__type_text_split_num"},
                        {
                            "~#field": {
                                "~:name": "markenart__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "score",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SYNTHETIC"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_designer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "farbanspruch__type_boolean",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_thumbnail_hash__type_string_mv"},
                        {
                            "~#field": {
                                "~:name": "ra_teillizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_erfinder__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "id"},
                        {
                            "~#field": {
                                "~:name": "gesuchsnummer__type_text_split_num",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "wdlklassennummernformatiert__type_string"},
                        {
                            "~#field": {
                                "~:name": "wdltext__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_ausschliesslichelizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "markentyp__type_i18n"},
                        {"~#field": "indextime"},
                        {
                            "~#field": {
                                "~:name": "ra_betreibungsamt__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_verfuegungsbeschraenker__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "schutzablaufdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_konkursamt__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "titel__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "schutztitelstatus__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "createtime__type_date"},
                        {"~#field": "changetime__type_date"},
                        {"~#field": "datastore_timestamp__type_date"},
                        {
                            "~#field": {
                                "~:name": "ra_inhaber__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "markentyp__type_i18n_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "wortbestandteil__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_print_hash__type_string_mv"},
                        {
                            "~#field": {
                                "~:name": "ra_lizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "wdlklassennummer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                    ],
                    "~:sort": [
                        {
                            "~#tpl": [
                                {
                                    "~#field": {
                                        "~:name": "eintragungsdatum__type_date",
                                        "~:meta": {
                                            "~#set": [
                                                {
                                                    "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                                }
                                            ]
                                        },
                                    }
                                },
                                {
                                    "~#enum": "~:ch.ipi.search.common.backend.query.SortOrder/DESC"
                                },
                            ]
                        },
                        {
                            "~#tpl": [
                                {"~#field": "id"},
                                {
                                    "~#enum": "~:ch.ipi.search.common.backend.query.SortOrder/DESC"
                                },
                            ]
                        },
                    ],
                    "~:meta": {
                        "~#lmm": {
                            "session": ["R5c156814"],
                            "remote-addr": ["202.137.119.4"],
                        }
                    },
                    "~:cursor": {"~#opt": "*"},
                    "~:count-values": [
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschgrund__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "verkehrsdurchsetzung__type_boolean",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztitelstadium__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "officeorigincode__type_string",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "doctype",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "ipikontoid__type_string",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztiteltyp__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "markenart__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "farbanspruch__type_boolean",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztitelstatus__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "markentyp__type_i18n_mv",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "wdlklassennummer__type_text_mv",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                        },
                    ],
                    "~:count-queries": [
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_WEEK"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_MONTH"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_YEAR"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "publikationsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "hinterlegungsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#LAST_WEEK"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "eintragungsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#LAST_YEAR"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "schutzablaufdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                    ],
                }
            },
        }
    }


def post_data_from_oldest(items_size, cursor):
    """Cursor is needed to get the next results"""

    return {
        "~#resultmeta": {
            "~:page-items": items_size,
            "~:total-items": 941843,
            "~:max-score": {"~#opt": 1.0},
            "~:cursor": {"~#opt": cursor},
            "~:processing-time": {"~#millis": 205},
            "~:query": {
                "~#query": {
                    "~:target": {"~#queryTarget": "chmarke"},
                    "~:page-size": items_size,
                    "~:extra-params": {
                        "~#lmm": {
                            "qf": [
                                "titel__type_text^6.0 wortbestandteil__type_text^5.0 markennummer__type_int^4.0 markennummer_formatiert__type_string^4.0 gesuchsnummer__type_text_split_num^3.0 ra_inhaber__type_text_mv^2.0 ra_vertreter__type_text_mv^1.0 wdltext__type_text^1.0 wdlklassennummer__type_text_mv^1.0 markennummer__type_text_split_num^4.0"
                            ]
                        }
                    },
                    "~:select": [
                        {"~#field": "datastore_checksum__type_string"},
                        {"~#field": "verfahrenssprache__type_string"},
                        {
                            "~#field": {
                                "~:name": "ra_nutzniesser__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_pfandnehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "farbanspruch__type_boolean",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "erneuertemarke__type_boolean"},
                        {
                            "~#field": "quelleersteveroeffentlichung_publikationsziel__type_i18n"
                        },
                        {
                            "~#field": {
                                "~:name": "doctype",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_inhaber__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "hinterlegungsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_unterlizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "verfahrenssprache__type_i18n"},
                        {"~#field": "wdl__type_text_mv"},
                        {
                            "~#field": {
                                "~:name": "markenart__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": "quelleersteveroeffentlichung_ausgabe__type_string"
                        },
                        {
                            "~#field": {
                                "~:name": "markentyp__type_i18n_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "wdlklassennummer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "verkehrsdurchsetzung__type_i18n"},
                        {
                            "~#field": {
                                "~:name": "ipikontoid__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "anmeldereferenz__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "titel__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "gesuchsnummer__type_text_split_num",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "farbanspruch__type_text"},
                        {
                            "~#field": {
                                "~:name": "schutztitelstatus__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_teillizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "schutzablaufdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_vertreter__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_screen_hash__type_string_mv"},
                        {"~#field": "markennummer__type_int"},
                        {
                            "~#field": {
                                "~:name": "wortbestandteil__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "spezialmarken__type_i18n_mv"},
                        {
                            "~#field": {
                                "~:name": "markennummer_formatiert__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "markennummer__type_text_split_num"},
                        {
                            "~#field": {
                                "~:name": "eintragungsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "publikationsdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_designer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_erfinder__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_thumbnail_hash__type_string_mv"},
                        {
                            "~#field": {
                                "~:name": "schutztiteltyp__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "id"},
                        {
                            "~#field": {
                                "~:name": "ra_betreibungsamt__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "wdlklassennummernformatiert__type_string"},
                        {
                            "~#field": {
                                "~:name": "loeschdatum__type_date",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "markentyp__type_i18n"},
                        {"~#field": "indextime"},
                        {
                            "~#field": {
                                "~:name": "ra_konkursamt__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "loeschgrund__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_ausschliesslichelizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "score",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SYNTHETIC"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "wdltext__type_text",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "createtime__type_date"},
                        {
                            "~#field": {
                                "~:name": "schutztitelstadium__type_i18n",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "changetime__type_date"},
                        {
                            "~#field": {
                                "~:name": "_version_",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SYNTHETIC"
                                        }
                                    ]
                                },
                            }
                        },
                        {"~#field": "datastore_timestamp__type_date"},
                        {
                            "~#field": {
                                "~:name": "verkehrsdurchsetzung__type_boolean",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "ra_lizenznehmer__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {"~#field": "bild_print_hash__type_string_mv"},
                        {
                            "~#field": {
                                "~:name": "ra_verfuegungsbeschraenker__type_text_mv",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/MULTI"
                                        },
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                        },
                                    ]
                                },
                            }
                        },
                        {
                            "~#field": {
                                "~:name": "officeorigincode__type_string",
                                "~:meta": {
                                    "~#set": [
                                        {
                                            "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                        }
                                    ]
                                },
                            }
                        },
                    ],
                    "~:sort": [
                        {
                            "~#tpl": [
                                {
                                    "~#field": {
                                        "~:name": "eintragungsdatum__type_date",
                                        "~:meta": {
                                            "~#set": [
                                                {
                                                    "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                                }
                                            ]
                                        },
                                    }
                                },
                                {
                                    "~#enum": "~:ch.ipi.search.common.backend.query.SortOrder/ASC"
                                },
                            ]
                        },
                        {
                            "~#tpl": [
                                {"~#field": "id"},
                                {
                                    "~#enum": "~:ch.ipi.search.common.backend.query.SortOrder/DESC"
                                },
                            ]
                        },
                    ],
                    "~:meta": {
                        "~#lmm": {
                            "session": ["R4d6218c0"],
                            "remote-addr": ["202.137.119.4"],
                        }
                    },
                    "~:cursor": {"~#opt": "*"},
                    "~:count-values": [
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "farbanspruch__type_boolean",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "doctype",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "markenart__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "markentyp__type_i18n_mv",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "wdlklassennummer__type_text_mv",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/SNIPPETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "ipikontoid__type_string",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztitelstatus__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztiteltyp__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschgrund__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutztitelstadium__type_i18n",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "verkehrsdurchsetzung__type_boolean",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                        {
                            "~:include-non-matched?": True,
                            "~:min-count": {"~#opt": 0},
                            "~:field": {
                                "~#field": {
                                    "~:name": "officeorigincode__type_string",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                        },
                    ],
                    "~:count-queries": [
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "hinterlegungsdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "hinterlegungsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "hinterlegungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "schutzablaufdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "schutzablaufdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "schutzablaufdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#LAST_WEEK"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "eintragungsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#LAST_YEAR"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "eintragungsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "eintragungsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            }
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_WEEK"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_MONTH"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {
                                "~#opt": "publikationsdatum__type_date#LAST_YEAR"
                            },
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "publikationsdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "publikationsdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_WEEK"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-7DAYS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_MONTH"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1MONTHS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#LAST_YEAR"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[NOW-1YEARS/DAY TO NOW]",
                        },
                        {
                            "~:key": {"~#opt": "loeschdatum__type_date#ALL"},
                            "~:include-non-matched?": True,
                            "~:field": {
                                "~#field": {
                                    "~:name": "loeschdatum__type_date",
                                    "~:meta": {
                                        "~#set": [
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/NULLABLE"
                                            },
                                            {
                                                "~#enum": "~:ch.ipi.search.common.backend.query.FieldMetadata$Flag/FACETABLE"
                                            },
                                        ]
                                    },
                                }
                            },
                            "~:constraint": "[* TO *]",
                        },
                    ],
                }
            },
        }
    }
