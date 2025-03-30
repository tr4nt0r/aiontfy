"""Exceptions for aiontfy."""


class NtfyException(Exception):  # noqa: N818
    """Base ntfy exception."""


class NtfyHTTPError(NtfyException):
    """Base class for HTTP errors."""

    def __init__(
        self, code: int, http: int, error: str, link: str | None = None
    ) -> None:
        """
        Initialize the exception with a code, HTTP status, error message, and link.

        Parameters
        ----------
        code : int
            The error code.
        http : int
            The HTTP status code.
        error : str
            The error message.
        link : str, optional
            A link to more information about the error.

        """
        self.code = code
        self.http = http
        self.error = error
        self.link = link

        super().__init__(self.error)


class NtfyConnectionError(NtfyException):
    """Connection error."""


class NtfyTimeoutError(NtfyException):
    """Timeout error."""


class NtfyUnknownError(NtfyException):
    """Unexpected HTTP errors."""


class NtfyBadRequestError(NtfyHTTPError):
    """400 Bad Request."""


class NtfyUnauthorizedError(NtfyHTTPError):
    """401 Unauthorized."""


class NtfyForbiddenError(NtfyHTTPError):
    """403 Forbidden."""


class NtfyNotFoundError(NtfyHTTPError):
    """404 Not Found."""


class NtfyConflictError(NtfyHTTPError):
    """409 Conflict."""


class NtfyGoneError(NtfyHTTPError):
    """410 Gone."""


class NtfyRequestEntityTooLargeError(NtfyHTTPError):
    """413 Request Entity Too Large."""


class NtfyTooManyRequestsError(NtfyHTTPError):
    """429 Too Many Requests."""


class NtfyInternalServerError(NtfyHTTPError):
    """500 Internal Server Error."""


class NtfyInsufficientStorageError(NtfyHTTPError):
    """507 Insufficient Storage."""


class NtfyBadRequestEmailDisabledError(NtfyBadRequestError):
    """40001 E-mail notifications are not enabled."""


class NtfyBadRequestDelayNoCacheError(NtfyBadRequestError):
    """40002 Cannot disable cache for delayed message."""


class NtfyBadRequestDelayNoEmailError(NtfyBadRequestError):
    """40003 Delayed e-mail notifications are not supported."""


class NtfyBadRequestDelayCannotParseError(NtfyBadRequestError):
    """40004 Invalid delay parameter: unable to parse delay."""


class NtfyBadRequestDelayTooSmallError(NtfyBadRequestError):
    """40005 Invalid delay parameter: too small."""


class NtfyBadRequestDelayTooLargeError(NtfyBadRequestError):
    """40006 Invalid delay parameter: too large."""


class NtfyBadRequestPriorityInvalidError(NtfyBadRequestError):
    """40007 Invalid priority parameter."""


class NtfyBadRequestSinceInvalidError(NtfyBadRequestError):
    """40008 Invalid since parameter."""


class NtfyBadRequestTopicInvalidError(NtfyBadRequestError):
    """40009 Invalid request: topic invalid."""


class NtfyBadRequestTopicDisallowedError(NtfyBadRequestError):
    """40010 Invalid request: topic name is not allowed."""


class NtfyBadRequestMessageNotUTF8Error(NtfyBadRequestError):
    """40011 Invalid request: message must be UTF-8 encoded."""


class NtfyBadRequestAttachmentURLInvalidError(NtfyBadRequestError):
    """40013 Invalid request: attachment URL is invalid."""


class NtfyBadRequestAttachmentsDisallowedError(NtfyBadRequestError):
    """40014 Invalid request: attachments not allowed."""


class NtfyBadRequestAttachmentsExpiryBeforeDeliveryError(NtfyBadRequestError):
    """40015 Invalid request: attachment expiry before delayed delivery date."""


class NtfyBadRequestWebSocketsUpgradeHeaderMissingError(NtfyBadRequestError):
    """40016 Invalid request: client not using the websocket protocol."""


class NtfyBadRequestMessageJSONInvalidError(NtfyBadRequestError):
    """40017 Invalid request: request body must be message JSON."""


class NtfyBadRequestActionsInvalidError(NtfyBadRequestError):
    """40018 Invalid request: actions invalid."""


class NtfyBadRequestMatrixMessageInvalidError(NtfyBadRequestError):
    """40019 Invalid request: Matrix JSON invalid."""


class NtfyBadRequestIconURLInvalidError(NtfyBadRequestError):
    """40021 Invalid request: icon URL is invalid."""


class NtfyBadRequestSignupNotEnabledError(NtfyBadRequestError):
    """40022 Invalid request: signup not enabled."""


class NtfyBadRequestNoTokenProvidedError(NtfyBadRequestError):
    """40023 Invalid request: no token provided."""


class NtfyBadRequestJSONInvalidError(NtfyBadRequestError):
    """40024 Invalid request: request body must be valid JSON."""


class NtfyBadRequestPermissionInvalidError(NtfyBadRequestError):
    """40025 Invalid request: incorrect permission string."""


class NtfyBadRequestIncorrectwordConfirmationError(NtfyBadRequestError):
    """40026 Invalid request: word confirmation is not correct."""


class NtfyBadRequestNotAPaidUserError(NtfyBadRequestError):
    """40027 Invalid request: not a paid user."""


class NtfyBadRequestBillingRequestInvalidError(NtfyBadRequestError):
    """40028 Invalid request: not a valid billing request."""


class NtfyBadRequestBillingSubscriptionExistsError(NtfyBadRequestError):
    """40029 Invalid request: billing subscription already exists."""


class NtfyBadRequestTierInvalidError(NtfyBadRequestError):
    """40030 Invalid request: tier does not exist."""


class NtfyBadRequestUserNotFoundError(NtfyBadRequestError):
    """40031 Invalid request: user does not exist."""


class NtfyBadRequestPhoneCallsDisabledError(NtfyBadRequestError):
    """40032 Invalid request: calling is disabled."""


class NtfyBadRequestPhoneNumberInvalidError(NtfyBadRequestError):
    """40033 Invalid request: phone number invalid."""


class NtfyBadRequestPhoneNumberNotVerifiedError(NtfyBadRequestError):
    """40034 Invalid request: phone number not verified."""


class NtfyBadRequestAnonymousCallsNotAllowedError(NtfyBadRequestError):
    """40035 Invalid request: anonymous phone calls are not allowed."""


class NtfyBadRequestPhoneNumberVerifyChannelInvalidError(NtfyBadRequestError):
    """40036 Invalid request: verification channel must be 'sms' or 'call'."""


class NtfyBadRequestDelayNoCallError(NtfyBadRequestError):
    """40037 Invalid request: delayed call notifications are not supported."""


class NtfyBadRequestWebPushSubscriptionInvalidError(NtfyBadRequestError):
    """40038 Invalid request: web push payload malformed."""


class NtfyBadRequestWebPushEndpointUnknownError(NtfyBadRequestError):
    """40039 Invalid request: web push endpoint unknown."""


class NtfyBadRequestWebPushTopicCountTooHighError(NtfyBadRequestError):
    """40040 Invalid request: too many web push topic subscriptions."""


class NtfyBadRequestTemplateMessageTooLargeError(NtfyBadRequestError):
    """40041 Invalid request: message or title is too large after replacing template."""


class NtfyBadRequestTemplateMessageNotJSONError(NtfyBadRequestError):
    """40042 Invalid request: message body must be JSON if templating is enabled."""


class NtfyBadRequestTemplateInvalidError(NtfyBadRequestError):
    """40043 Invalid request: could not parse template."""


class NtfyBadRequestTemplateDisallowedFunctionCallsError(NtfyBadRequestError):
    """40044 Invalid request: template contains disallowed function calls."""


class NtfyBadRequestTemplateExecuteFailedError(NtfyBadRequestError):
    """40045 Invalid request: template execution failed."""


class NtfyBadRequestInvalidUsernameError(NtfyBadRequestError):
    """40046 Invalid request: invalid username."""


# 404 Not Found Errors
class NtfyNotFoundPageError(NtfyNotFoundError):
    """40401 Page not found."""


# 401 Unauthorized Errors
class NtfyUnauthorizedAuthenticationError(NtfyUnauthorizedError):
    """40101 Unauthorized."""


# 403 Forbidden Errors
class NtfyForbiddenAccessError(NtfyForbiddenError):
    """40301 Forbidden."""


# 409 Conflict Errors
class NtfyConflictUserExistsError(NtfyConflictError):
    """40901 Conflict: user already exists."""


class NtfyConflictTopicReservedError(NtfyConflictError):
    """40902 Conflict: access control entry for topic or topic pattern already exists."""


class NtfyConflictSubscriptionExistsError(NtfyConflictError):
    """40903 Conflict: topic subscription already exists."""


class NtfyConflictPhoneNumberExistsError(NtfyConflictError):
    """40904 Conflict: phone number already exists."""


# 410 Gone Errors
class NtfyGonePhoneVerificationExpiredError(NtfyGoneError):
    """41001 Phone number verification expired or does not exist."""


# 413 Request Entity Too Large Errors
class NtfyRequestEntityTooLargeAttachmentError(NtfyRequestEntityTooLargeError):
    """41301 Attachment too large, or bandwidth limit reached."""


class NtfyRequestEntityTooLargeMatrixRequestError(NtfyRequestEntityTooLargeError):
    """41302 Matrix request is larger than the max allowed length."""


class NtfyRequestEntityTooLargeJSONBodyError(NtfyRequestEntityTooLargeError):
    """41303 JSON body too large."""


# 429 Too Many Requests Errors
class NtfyTooManyRequestsLimitRequestsError(NtfyTooManyRequestsError):
    """42901 Limit reached: too many requests."""


class NtfyTooManyRequestsLimitEmailsError(NtfyTooManyRequestsError):
    """42902 Limit reached: too many emails."""


class NtfyTooManyRequestsLimitSubscriptionsError(NtfyTooManyRequestsError):
    """42903 Limit reached: too many active subscriptions."""


class NtfyTooManyRequestsLimitTotalTopicsError(NtfyTooManyRequestsError):
    """42904 Limit reached: the total number of topics on the server has been reached."""


class NtfyTooManyRequestsLimitAttachmentBandwidthError(NtfyTooManyRequestsError):
    """42905 Limit reached: daily bandwidth reached."""


class NtfyTooManyRequestsLimitAccountCreationError(NtfyTooManyRequestsError):
    """42906 Limit reached: too many accounts created."""


class NtfyTooManyRequestsLimitReservationsError(NtfyTooManyRequestsError):
    """42907 Limit reached: too many topic reservations for this user."""


class NtfyTooManyRequestsLimitMessagesError(NtfyTooManyRequestsError):
    """42908 Limit reached: daily message quota reached."""


class NtfyTooManyRequestsLimitAuthFailureError(NtfyTooManyRequestsError):
    """42909 Limit reached: too many auth failures."""


class NtfyTooManyRequestsLimitCallsError(NtfyTooManyRequestsError):
    """42910 Limit reached: daily phone call quota reached."""


# 500 Internal Server Error
class NtfyInternalErrorInvalidPathError(NtfyInternalServerError):
    """50002 Internal server error: invalid path."""


class NtfyInternalErrorMissingBaseURLError(NtfyInternalServerError):
    """50003 Internal server error: base-url must be configured for this feature."""


class NtfyInternalErrorWebPushUnableToPublishError(NtfyInternalServerError):
    """50004 Internal server error: unable to publish web push message."""


# 507 Insufficient Storage Errors
class NtfyInsufficientStorageUnifiedPushError(NtfyInsufficientStorageError):
    """50701 Cannot publish to UnifiedPush topic without previously active subscriber."""


def raise_http_error(code: int, http: int, error: str, link: str | None = None) -> None:
    """Raise an appropriate HTTP error based on the provided error code.

    Parameters
    ----------
    code : int
        The specific error code to raise.
    http : int
        The HTTP status code associated with the error.
    error : str
        A description of the error.
    link : str, optional
        A URL link providing more information about the error.

    Raises
    ------
    NtfyBadRequestError
        If the error code is 400.
    NtfyUnauthorizedError
        If the error code is 401.
    NtfyForbiddenError
        If the error code is 403.
    NtfyNotFoundError
        If the error code is 404.
    NtfyConflictError
        If the error code is 409.
    NtfyGoneError
        If the error code is 410.
    NtfyRequestEntityTooLargeError
        If the error code is 413.
    NtfyTooManyRequestsError
        If the error code is 429.
    NtfyInternalServerError
        If the error code is 500.
    NtfyInsufficientStorageError
        If the error code is 507.
    NtfyUnknownError
        If the error code is not recognized.
    """
    error_map = {
        400: NtfyBadRequestError,
        401: NtfyUnauthorizedError,
        403: NtfyForbiddenError,
        404: NtfyNotFoundError,
        409: NtfyConflictError,
        410: NtfyGoneError,
        413: NtfyRequestEntityTooLargeError,
        429: NtfyTooManyRequestsError,
        500: NtfyInternalServerError,
        507: NtfyInsufficientStorageError,
        40001: NtfyBadRequestEmailDisabledError,
        40002: NtfyBadRequestDelayNoCacheError,
        40003: NtfyBadRequestDelayNoEmailError,
        40004: NtfyBadRequestDelayCannotParseError,
        40005: NtfyBadRequestDelayTooSmallError,
        40006: NtfyBadRequestDelayTooLargeError,
        40007: NtfyBadRequestPriorityInvalidError,
        40008: NtfyBadRequestSinceInvalidError,
        40009: NtfyBadRequestTopicInvalidError,
        40010: NtfyBadRequestTopicDisallowedError,
        40011: NtfyBadRequestMessageNotUTF8Error,
        40013: NtfyBadRequestAttachmentURLInvalidError,
        40014: NtfyBadRequestAttachmentsDisallowedError,
        40015: NtfyBadRequestAttachmentsExpiryBeforeDeliveryError,
        40016: NtfyBadRequestWebSocketsUpgradeHeaderMissingError,
        40017: NtfyBadRequestMessageJSONInvalidError,
        40018: NtfyBadRequestActionsInvalidError,
        40019: NtfyBadRequestMatrixMessageInvalidError,
        40021: NtfyBadRequestIconURLInvalidError,
        40022: NtfyBadRequestSignupNotEnabledError,
        40023: NtfyBadRequestNoTokenProvidedError,
        40024: NtfyBadRequestJSONInvalidError,
        40025: NtfyBadRequestPermissionInvalidError,
        40026: NtfyBadRequestIncorrectwordConfirmationError,
        40027: NtfyBadRequestNotAPaidUserError,
        40028: NtfyBadRequestBillingRequestInvalidError,
        40029: NtfyBadRequestBillingSubscriptionExistsError,
        40030: NtfyBadRequestTierInvalidError,
        40031: NtfyBadRequestUserNotFoundError,
        40032: NtfyBadRequestPhoneCallsDisabledError,
        40033: NtfyBadRequestPhoneNumberInvalidError,
        40034: NtfyBadRequestPhoneNumberNotVerifiedError,
        40035: NtfyBadRequestAnonymousCallsNotAllowedError,
        40036: NtfyBadRequestPhoneNumberVerifyChannelInvalidError,
        40037: NtfyBadRequestDelayNoCallError,
        40038: NtfyBadRequestWebPushSubscriptionInvalidError,
        40039: NtfyBadRequestWebPushEndpointUnknownError,
        40040: NtfyBadRequestWebPushTopicCountTooHighError,
        40041: NtfyBadRequestTemplateMessageTooLargeError,
        40042: NtfyBadRequestTemplateMessageNotJSONError,
        40043: NtfyBadRequestTemplateInvalidError,
        40044: NtfyBadRequestTemplateDisallowedFunctionCallsError,
        40045: NtfyBadRequestTemplateExecuteFailedError,
        40046: NtfyBadRequestInvalidUsernameError,
        40401: NtfyNotFoundPageError,
        40101: NtfyUnauthorizedAuthenticationError,
        40301: NtfyForbiddenAccessError,
        40901: NtfyConflictUserExistsError,
        40902: NtfyConflictTopicReservedError,
        40903: NtfyConflictSubscriptionExistsError,
        40904: NtfyConflictPhoneNumberExistsError,
        41001: NtfyGonePhoneVerificationExpiredError,
        41301: NtfyRequestEntityTooLargeAttachmentError,
        41302: NtfyRequestEntityTooLargeMatrixRequestError,
        41303: NtfyRequestEntityTooLargeJSONBodyError,
        42901: NtfyTooManyRequestsLimitRequestsError,
        42902: NtfyTooManyRequestsLimitEmailsError,
        42903: NtfyTooManyRequestsLimitSubscriptionsError,
        42904: NtfyTooManyRequestsLimitTotalTopicsError,
        42905: NtfyTooManyRequestsLimitAttachmentBandwidthError,
        42906: NtfyTooManyRequestsLimitAccountCreationError,
        42907: NtfyTooManyRequestsLimitReservationsError,
        42908: NtfyTooManyRequestsLimitMessagesError,
        42909: NtfyTooManyRequestsLimitAuthFailureError,
        42910: NtfyTooManyRequestsLimitCallsError,
        50002: NtfyInternalErrorInvalidPathError,
        50003: NtfyInternalErrorMissingBaseURLError,
        50004: NtfyInternalErrorWebPushUnableToPublishError,
        50701: NtfyInsufficientStorageUnifiedPushError,
    }
    if error_class := error_map.get(code, error_map.get(http)):
        raise error_class(code, http, error, link)
    raise NtfyUnknownError
