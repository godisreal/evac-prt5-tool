MODULE DEVICE_VARIABLES
 
USE PRECISION_PARAMETERS
IMPLICIT NONE

CHARACTER(255), PARAMETER :: devcid='$Id$'
CHARACTER(255), PARAMETER :: devcrev='$Revision$'
CHARACTER(255), PARAMETER :: devcdate='$Date$'

LOGICAL :: GAS_CELL_RAD_FLUX=.FALSE.,CONDUIT=.FALSE.
INTEGER, POINTER, DIMENSION(:) :: GAS_CELL_RAD_DEVC_INDEX
INTEGER :: N_GAS_CELL_RAD_DEVC=0

TYPE PROPERTY_TYPE
   REAL(EB) :: BEAD_DIAMETER,BEAD_EMISSIVITY,RTI,ACTIVATION_TEMPERATURE,ACTIVATION_OBSCURATION, &
               ALPHA_E,ALPHA_C,BETA_E,BETA_C,CHARACTERISTIC_VELOCITY,DROPLET_VELOCITY,FLOW_RATE,FLOW_TAU,GAUGE_TEMPERATURE, &
               INITIAL_TEMPERATURE,K_FACTOR,C_FACTOR,OPERATING_PRESSURE,OFFSET,SPRAY_ANGLE(2), &
               CABLE_DIAMETER,CABLE_JACKET_THICKNESS,CABLE_FAILURE_TEMPERATURE,CABLE_MASS_PER_LENGTH, &
               CONDUIT_DIAMETER,CONDUIT_THICKNESS
   INTEGER  :: PDPA_M=3,PDPA_N=2
   LOGICAL  :: PDPA_U=.FALSE.,PDPA_V=.FALSE.,PDPA_W=.FALSE.,PDPA_COUNT=.FALSE.
   REAL(EB) :: PDPA_START=0._EB,PDPA_END=1.E6,PDPA_RADIUS=0.1_EB
   REAL, POINTER, DIMENSION(:) :: TABLE_ROW
   INTEGER  :: PART_INDEX,FLOW_RAMP_INDEX,SPRAY_PATTERN_INDEX,SPEC_INDEX=0
   CHARACTER(30) :: SMOKEVIEW_ID,PART_ID,ID,QUANTITY,TABLE_ID,SPEC_ID='null'
END TYPE PROPERTY_TYPE

TYPE DEVICE_TYPE
   REAL(EB) :: T,X,Y,Z,X1,X2,Y1,Y2,Z1,Z2,INSTANT_VALUE,VALUE,DEPTH,TMP_L,Y_C,OBSCURATION,DELAY,ROTATION,&
               SETPOINT, T_CHANGE=1000000._EB,BYPASS_FLOWRATE,DT,TOTAL_FLOWRATE,FLOWRATE
   REAL(EB) :: PDPA_NUMER=0._EB,PDPA_DENUM=0._EB
   INTEGER  :: PDPA_GROUP
   REAL(EB), POINTER, DIMENSION(:) :: D_PATH,TIME_ARRAY
   REAL(EB), POINTER, DIMENSION(:,:) :: YY_SOOT, ILW
   REAL(EB), DIMENSION(3) :: ORIENTATION
   INTEGER  :: OUTPUT_INDEX,IOR,IW,COUNT,ORDINAL,I,J,K,MESH,I1=-1,I2=-1,J1=-1,J2=-1,K1=-1,K2=-1,I_DEPTH,N_PATH,N_T_E,PROP_INDEX,&
               TRIP_DIRECTION,CTRL_INDEX,N_INPUTS,VIRTUAL_WALL_INDEX=0,SURF_INDEX=-1,SPEC_INDEX=0,PART_INDEX=0
   INTEGER, POINTER, DIMENSION(:) :: DEVC_INDEX
   INTEGER, POINTER, DIMENSION(:) :: I_PATH,J_PATH,K_PATH
   REAL(EB),  POINTER, DIMENSION(:) :: Y_E,T_E
   CHARACTER(30) :: ID,PROP_ID,QUANTITY,CTRL_ID,DEVC_ID,STATISTICS='null',SURF_ID,PART_ID='null',SPEC_ID='null',MATL_ID='null', &
                    SMOKEVIEW_BAR_LABEL
   CHARACTER(60) :: SMOKEVIEW_LABEL
   LOGICAL :: INITIAL_STATE,CURRENT_STATE,LATCH,PRIOR_STATE,GAS_CELL_RAD_FLUX=.FALSE.
END TYPE DEVICE_TYPE

TYPE CABLE_TYPE
   REAL(EB) :: DIAMETER,FAILURE_TEMPERATURE,MASS_PER_LENGTH
   INTEGER :: PROP_INDEX
END TYPE CABLE_TYPE

! Device arrays

INTEGER :: N_PROP,N_DEVC,N_CABL=0
TYPE (PROPERTY_TYPE),  DIMENSION(:), ALLOCATABLE, TARGET :: PROPERTY
TYPE (DEVICE_TYPE),  DIMENSION(:), ALLOCATABLE, TARGET :: DEVICE
TYPE (CABLE_TYPE),  DIMENSION(:), ALLOCATABLE, TARGET :: CABLE

CONTAINS

SUBROUTINE GET_REV_devc(MODULE_REV,MODULE_DATE)
INTEGER,INTENT(INOUT) :: MODULE_REV
CHARACTER(255),INTENT(INOUT) :: MODULE_DATE

WRITE(MODULE_DATE,'(A)') devcrev(INDEX(devcrev,':')+1:LEN_TRIM(devcrev)-2)
READ (MODULE_DATE,'(I5)') MODULE_REV
WRITE(MODULE_DATE,'(A)') devcdate

END SUBROUTINE GET_REV_devc

END MODULE DEVICE_VARIABLES

MODULE CONTROL_VARIABLES
! Variables for evaluating control functions
USE PRECISION_PARAMETERS

IMPLICIT NONE

TYPE CONTROL_TYPE
   LOGICAL :: SPECIFIED_STATE=.FALSE.,INITIAL_STATE=.FALSE.,CURRENT_STATE=.FALSE.,PRIOR_STATE=.FALSE.,LATCH=.TRUE.,UPDATED=.FALSE.
   INTEGER :: CONTROL_INDEX=0,CYCLES=1,N_INPUTS=0,RAMP_INDEX=0,MESH=1,N=1,ON_BOUND=0
   INTEGER, POINTER, DIMENSION (:) :: INPUT,INPUT_TYPE
   REAL(EB) :: SETPOINT(2)=1000000._EB, DELAY=0._EB, T_CHANGE=1000000._EB ,CYCLE_TIME=1000000._EB
   CHARACTER(30) :: ID='null',RAMP_ID='null',INPUT_ID(40)='null'
END TYPE CONTROL_TYPE

TYPE (CONTROL_TYPE),  DIMENSION(:), ALLOCATABLE, TARGET :: CONTROL

INTEGER, PARAMETER :: AND_GATE=1, OR_GATE=2, XOR_GATE=3, X_OF_N_GATE=4, TIME_DELAY=5, DEADBAND=6, CYCLING=7, &
                      CUSTOM=8,KILL=9,CORE_DUMP=10,DEVICE_INPUT=1, CONTROL_INPUT=2

INTEGER :: N_CTRL, N_CTRL_FILES

END MODULE CONTROL_VARIABLES
