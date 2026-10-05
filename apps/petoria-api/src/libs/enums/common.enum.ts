import { registerEnumType } from '@nestjs/graphql';

export enum Messages {
	SOMETHING_WENT_WRONG = 'Something went wrong!',
	NO_DATA_FOUND = 'No data is found!',
	CREATE_FAILED = 'Create is failed!',
	UPDATE_FAILED = 'Update is failed!',
	REMOVE_FAILED = 'Remove failed!',
	UPLOAD_FAILED = 'Upload failed!',
	BAD_REQUEST = 'Bad Request',

	NO_MEMBER_NICK = 'no member with that member nick!',
	BLOCKED_USER = 'You have been blocked, please contact admin!',
	WRONG_PASSWORD = 'wrong password entered, please try again',
	USED_NICK_PHONE = 'you are inserting already used nick or phone!',
	NOT_AUTHENTICATED = 'You are not authenticated, login first!',
	TOKEN_CREATION_FAILED = 'Token creation error!',
	TOKEN_NOT_EXIST = 'Bearer Token is not provided!',
	ONLY_SPECIFIC_ROLES_ALLOWED = 'Allowed only for members with specific roles!',
	NOT_ALLOWED_REQUEST = 'Not Allowed Request!',
	PROVIDE_ALLOWED_FORMAT = 'Please provide jpg, jpeg, or png images!',
	SELF_SUBSCRIPTION_DENIED = 'Self subscription is denied!',
}

export enum Direction {
	ASC = 1,
	DESC = -1,
}
registerEnumType(Direction, {
	name: 'Direction',
});
