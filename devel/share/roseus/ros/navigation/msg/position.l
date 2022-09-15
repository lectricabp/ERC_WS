;; Auto-generated. Do not edit!


(when (boundp 'navigation::Position)
  (if (not (find-package "NAVIGATION"))
    (make-package "NAVIGATION"))
  (shadow 'Position (find-package "NAVIGATION")))
(unless (find-package "NAVIGATION::POSITION")
  (make-package "NAVIGATION::POSITION"))

(in-package "ROS")
;;//! \htmlinclude Position.msg.html


(defclass navigation::Position
  :super ros::object
  :slots (_id _x _z _angle ))

(defmethod navigation::Position
  (:init
   (&key
    ((:id __id) 0)
    ((:x __x) 0.0)
    ((:z __z) 0.0)
    ((:angle __angle) 0.0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _x (float __x))
   (setq _z (float __z))
   (setq _angle (float __angle))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; int16 _id
    2
    ;; float64 _x
    8
    ;; float64 _z
    8
    ;; float64 _angle
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _id
       (write-word _id s)
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _id
     (setq _id (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _angle
     (setq _angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get navigation::Position :md5sum-) "ac52e44dba22ebffb6e4c45e785ffdda")
(setf (get navigation::Position :datatype-) "navigation/Position")
(setf (get navigation::Position :definition-)
      "int16   id
float64 x
float64 z
float64 angle
")



(provide :navigation/Position "ac52e44dba22ebffb6e4c45e785ffdda")


